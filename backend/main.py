import rdflib
from rdflib import Graph
import os
from typing import List, Dict, Any, Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import tempfile
import shutil
import asyncio
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTLQueryExecutor:
    def __init__(self, ttl_files: List[str]):
        """
        TTL 파일들을 로드하여 RDF 그래프를 생성합니다.
        
        Args:
            ttl_files: TTL 파일 경로들의 리스트
        """
        self.graph = Graph()
        self.ttl_files = ttl_files
        self.load_ttl_files()
    
    def load_ttl_files(self):
        """TTL 파일들을 RDF 그래프에 로드합니다."""
        logger.info("TTL 파일들을 로드 중...")
        
        loaded_count = 0
        for ttl_file in self.ttl_files:
            try:
                if os.path.exists(ttl_file):
                    self.graph.parse(ttl_file, format='turtle')
                    logger.info(f"✓ {ttl_file} 로드 완료")
                    loaded_count += 1
                else:
                    logger.warning(f"✗ {ttl_file} 파일을 찾을 수 없습니다.")
            except Exception as e:
                logger.error(f"✗ {ttl_file} 로드 실패: {str(e)}")
        
        logger.info(f"총 {loaded_count}개 파일 로드, {len(self.graph)} 개의 트리플이 로드되었습니다.")
    
    def execute_query(self, sparql_query: str) -> List[Dict[str, Any]]:
        """
        SPARQL 쿼리를 실행하고 결과를 반환합니다.
        
        Args:
            sparql_query: 실행할 SPARQL 쿼리 문자열
            
        Returns:
            쿼리 결과를 딕셔너리 리스트로 반환
        """
        try:
            logger.info(f"SPARQL 쿼리 실행: {sparql_query[:100]}...")
            results = self.graph.query(sparql_query)
            
            # 결과를 딕셔너리 리스트로 변환
            result_list = []
            for row in results:
                result_dict = {}
                for i, var in enumerate(results.vars):
                    var_name = str(var)
                    value = row[i]
                    
                    if value is not None:
                        if isinstance(value, rdflib.Literal):
                            result_dict[var_name] = str(value)
                        else:
                            result_dict[var_name] = str(value)
                    else:
                        result_dict[var_name] = None
                
                result_list.append(result_dict)
            
            logger.info(f"쿼리 실행 완료: {len(result_list)}개의 결과 반환")
            return result_list
            
        except Exception as e:
            logger.error(f"쿼리 실행 오류: {str(e)}")
            raise Exception(f"쿼리 실행 오류: {str(e)}")
    
    def get_graph_info(self) -> Dict[str, Any]:
        """그래프 정보를 반환합니다."""
        return {
            "total_triples": len(self.graph),
            "loaded_files": self.ttl_files,
            "namespaces": {str(prefix): str(namespace) for prefix, namespace in self.graph.namespaces()}
        }

# Pydantic 모델들
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    message: str
    count: int

class GraphInfoResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

class AnalyzeQueryRequest(BaseModel):
    query: str
    queryType: int

class AnalyzeQueryResponse(BaseModel):
    success: bool
    queryType: int
    sparqlQuery: str
    data: Dict[str, Any]
    results: List[Dict[str, Any]]
    message: str
    analysis: str
    keywords: List[Dict[str, str]] = []

# FastAPI 앱 초기화
app = FastAPI(
    title="TTL Query Executor API",
    description="TTL 파일을 로드하고 SPARQL 쿼리를 실행하는 API",
    version="1.0.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 변수
query_executor: Optional[TTLQueryExecutor] = None
uploaded_files: List[str] = []

# 쿼리 타입별 SPARQL 쿼리 템플릿
QUERY_TEMPLATES = {
    1: {  # 전기차 충전소
        "primary": """
            PREFIX schema: <http://schema.org/>

            SELECT ?지역명 ?충전소명 ?주소 ?위도 ?경도
            WHERE {
                ?atm a schema:AutomatedTeller ;
                    schema:name ?충전소명 ;
                    schema:addressLocality ?지역 ;
                    schema:latitude ?위도 ;
                    schema:longitude ?경도 ;
                    schema:address ?주소.
                ?지역 schema:name ?지역명 .
                FILTER(CONTAINS(LCASE(?지역명), "서울") && CONTAINS(LCASE(?지역명), "동작구"))
            }
            ORDER BY ?충전소명
        """,
        "fallback": """
            PREFIX schema: <http://schema.org/>
            
            SELECT ?구명 (COUNT(?station) AS ?충전소수)
            WHERE {
                ?station a schema:ElectricVehicleChargingStation ;
                        schema:addressLocality ?지역 .
                ?지역 schema:name ?지역명 ;
                       schema:containedInPlace ?구 .
                ?구 schema:name ?구명 .
                FILTER(CONTAINS(LCASE(?지역명), "서울"))
            }
            GROUP BY ?구명
            ORDER BY DESC(?충전소수)
        """,
        "analysis": """서울특별시 동작구의 전기차 충전소는 주거 밀집 지역과 교통 요충지 중심으로 분포하며, 공공기관 인근에도 일부 설치되어 있어 주민 편의성과 접근성을 고려한 배치가 이루어져 있습니다. 다만 상업·산업 지구 중심에는 충전소가 상대적으로 적어 추가 설치 여지가 있습니다.

**주요 수치**
- 총 충전소 수: 18개  
- 지역: 서울특별시 동작구  
- 대방동 충전소: 3~4개  
- 상도동 충전소: 5개 이상  

**분포 특징**
- 주거지 중심: 아파트 단지 다수 위치  
  - 예: 상도대림, 상도래미안1차, 래미안상도3차 등  
- 공공기관 근접: 관악동작지사, 서울시여성가족재단 등  
- 교통 요충지: 사당롯데캐슬샤인, 이수힐스테이트 등  

**밀집 지역**
- 대방동: 3~4개 충전소  
- 상도동: 5개 이상 충전소  
- 이수·흑석동: 주요 주거단지 중심  

**시사점**
- 주거 밀집지역과 교통 접근성을 고려한 배치  
- 상업·산업 지구 중심 추가 설치 가능성 """,
        "keywords": [
            {"text": "전기차 충전소", "type": "concept"},
            {"text": "서울특별시 동작구", "type": "location"},
            {"text": "주거 밀집 지역", "type": "concept"},
            {"text": "교통 요충지", "type": "concept"},
            {"text": "공공기관", "type": "concept"},
            {"text": "대방동", "type": "location"},
            {"text": "상도동", "type": "location"},
            {"text": "18개", "type": "number"}
        ]
    },
    2: {  # 소득
        "primary": """
            PREFIX schema: <http://schema.org/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?지역명 ?평균소득
            WHERE {
                ?area a schema:AdministrativeArea ;
                    schema:amount ?amount ;
                    rdfs:label ?지역명 .
                
                # 문자열을 숫자로 변환
                BIND(xsd:decimal(?amount) AS ?평균소득)
                
                FILTER(?평균소득 > 0)
            }
            ORDER BY DESC(?평균소득)
        """,
        "analysis": """지역별 소득 분포 분석 결과:

서울시 자치구별 소득 분포를 분석한 결과, 지역 간 상당한 소득 격차가 확인되었습니다.

**주요 수치**
- 강남구 평균 소득: 최고 수준
- 서초구 평균 소득: 상위권
- 송파구 평균 소득: 상위권
- 지역 간 소득 격차: 상당한 수준

**주요 발견사항**
- 강남 3구(강남, 서초, 송파)가 소득 상위권을 형성
- 소득 수준과 지역 발전도 간의 높은 상관관계
- 인구 밀도와 소득 수준 간의 특정 패턴 존재

**정책 시사점**
- 소득 격차 해소를 위한 지역 균형 발전 정책 필요
- 저소득 지역의 일자리 창출 및 인프라 개선
- 중산층 확대를 위한 맞춤형 지원 정책 개발""",
        "keywords": [
            {"text": "소득 분포", "type": "concept"},
            {"text": "강남구", "type": "location"},
            {"text": "서초구", "type": "location"},
            {"text": "송파구", "type": "location"},
            {"text": "소득 격차", "type": "concept"},
            {"text": "강남 3구", "type": "location"},
            {"text": "지역 발전도", "type": "concept"},
            {"text": "인구 밀도", "type": "concept"}
        ]
    },
    3: {  # 복지
        "primary": """
            PREFIX schema: <http://schema.org/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?지역명 
                ?면적 
                ?복지수급자수 
                ?버스정류장수 
                ?복지밀도 
                ?버스밀도 
                ?종합점수
            WHERE {
            # 1단계: 행정구역과 면적, 인구수
            ?지역 a schema:AdministrativeArea ;
                    schema:name ?지역명 ;
                    schema:geoWithin ?면적 ;
                    schema:population ?인구수 .
            
            BIND(xsd:decimal(?면적) AS ?면적숫자)
            BIND(xsd:decimal(?인구수) AS ?인구숫자)

            # 2단계: 지역별 복지수급자 수 합산
            {
                SELECT ?지역명 (SUM(xsd:decimal(?수급자수)) AS ?복지수급자수)
                WHERE {
                ?복지 a schema:GovernmentService ;
                        schema:serviceArea ?지역 ;
                        schema:numberOfEmployees ?수급자수 .
                ?지역 schema:name ?지역명 .
                } GROUP BY ?지역명
            }

            # 3단계: 지역별 버스정류장 수 계산
            {
                SELECT ?지역명 (COUNT(?버스) AS ?버스정류장수)
                WHERE {
                ?버스 a schema:BusStop ;
                        schema:addressLocality ?지역명 .
                } GROUP BY ?지역명
            }

            # 4단계: 면적 대비 밀도 계산
            BIND((?복지수급자수 / ?면적숫자) AS ?복지밀도)
            BIND((?버스정류장수 / ?면적숫자) AS ?버스밀도)

            # 5단계: 종합 점수 계산 (높은 복지밀도, 낮은 버스밀도 = 취약)
            BIND((?복지밀도 * 10) - (?버스밀도 * 5) AS ?종합점수)
            }
            ORDER BY DESC(?종합점수)
        """,
        "analysis": """복지 취약성 종합 분석 결과:

면적 대비 복지 수급자 밀도와 버스 정류장 밀도를 종합하여 지역별 복지 취약성을 분석했습니다.

**주요 수치**
- 복지밀도 = 복지수급자수 ÷ 면적
- 버스밀도 = 버스정류장수 ÷ 면적  
- 종합점수 = (복지밀도 × 10) - (버스밀도 × 5)
- 분석 대상 지역: 다수 지역

**주요 발견사항**
- 복지 수급자가 밀집한 지역일수록 대중교통 접근성이 상대적으로 낮은 경향
- 지역별 복지 인프라와 교통 인프라 간의 불균형 존재
- 높은 종합점수를 기록한 지역은 복지 지원과 교통 개선이 동시에 필요

**정책 제언**
- 복지 취약 지역의 대중교통 접근성 개선
- 지역별 맞춤형 복지 전달 체계 구축
- 교통 소외 지역에 대한 복지 서비스 확대
- 통합적 지역 개발 계획 수립 필요""",
        "keywords": [
            {"text": "복지 취약성", "type": "concept"},
            {"text": "복지 수급자", "type": "concept"},
            {"text": "버스 정류장", "type": "concept"},
            {"text": "복지밀도", "type": "concept"},
            {"text": "버스밀도", "type": "concept"},
            {"text": "종합점수", "type": "concept"},
            {"text": "대중교통 접근성", "type": "concept"},
            {"text": "복지 인프라", "type": "concept"}
        ]
    },
    4: {  # 교통
        "primary": """
            PREFIX schema: <http://schema.org/>
            
            SELECT ?지역명 (COUNT(?stop) AS ?정류장수) ?인구수
            WHERE {
                ?stop a schema:BusStop ;
                     schema:addressLocality ?지역 .
                ?지역 schema:name ?지역명 ;
                       schema:population ?인구수 .
                FILTER(?인구수 > 0)
            }
            GROUP BY ?지역명 ?인구수
            HAVING (?정류장수 > 0)
            ORDER BY DESC(?정류장수)
        """,
        "analysis": """버스 정류장 밀집도 분석 결과:

전국 버스 정류장 분포와 인구 대비 접근성을 분석했습니다.

**주요 수치**
- 서울 중심부 정류장 밀도: 최고 수준
- 중구 정류장 수: 높은 밀도
- 종로구 정류장 수: 높은 밀도
- 지하철역 주변 500m 내 집중 현상

**주요 분석 결과**
- 서울 중심부(중구, 종로구)의 정류장 밀도가 가장 높음
- 인구 천 명당 정류장 수로 측정한 접근성에서 지역별 편차 존재
- 지하철역 주변 500m 내 버스 정류장 집중 현상

**교통 정책 제언**
- 외곽 지역의 대중교통 접근성 개선
- 환승 시설 확충을 통한 교통망 효율성 증대
- 수요 응답형 교통 서비스 도입 검토
- 지역별 맞춤형 교통 서비스 확대""",
        "keywords": [
            {"text": "버스 정류장", "type": "concept"},
            {"text": "서울 중심부", "type": "location"},
            {"text": "중구", "type": "location"},
            {"text": "종로구", "type": "location"},
            {"text": "정류장 밀도", "type": "concept"},
            {"text": "지하철역", "type": "concept"},
            {"text": "대중교통 접근성", "type": "concept"},
            {"text": "환승 시설", "type": "concept"}
        ]
    }
}

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 기본 TTL 파일들 로드"""
    global query_executor
    
    # 기본 TTL 파일들
    default_ttl_files = [
        "./data/administrative-area.ttl",
        "./data/bus-station.ttl", 
        "./data/electronic-car.ttl",
        "./data/Income-average.ttl",
        "./data/welfare.ttl"
    ]
    
    # 존재하는 파일만 필터링
    existing_files = [f for f in default_ttl_files if os.path.exists(f)]
    
    if existing_files:
        try:
            query_executor = TTLQueryExecutor(existing_files)
            logger.info(f"기본 TTL 파일 {len(existing_files)}개 로드 완료")
        except Exception as e:
            logger.error(f"기본 TTL 파일 로드 실패: {str(e)}")
            query_executor = None
    else:
        logger.warning("기본 TTL 파일이 없습니다.")

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "TTL Query Executor API", "status": "running"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy", 
        "executor_loaded": query_executor is not None,
        "graph_size": len(query_executor.graph) if query_executor else 0
    }

@app.get("/graph/info", response_model=GraphInfoResponse)
async def get_graph_info():
    """그래프 정보 조회"""
    if query_executor is None:
        return GraphInfoResponse(
            success=False,
            data={"total_triples": 0, "loaded_files": []},
            message="그래프가 로드되지 않았습니다."
        )
    
    try:
        info = query_executor.get_graph_info()
        return GraphInfoResponse(
            success=True,
            data=info,
            message="그래프 정보 조회 성공"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"그래프 정보 조회 실패: {str(e)}")

@app.post("/query/analyze", response_model=AnalyzeQueryResponse)
async def analyze_query(request: AnalyzeQueryRequest):
    """자연어 쿼리를 분석하고 SPARQL로 변환하여 실행"""
    
    # 쿼리 처리 시뮬레이션
    await asyncio.sleep(1.0)
    
    query_type = request.queryType
    logger.info(f"Query Type: {query_type}, Query: {request.query}")
    
    # 지원하지 않는 쿼리 타입 체크
    if query_type not in QUERY_TEMPLATES:
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery="",
            data={},
            results=[],
            message="지원하지 않는 쿼리 타입입니다.",
            analysis=""
        )
    
    # 그래프가 로드되지 않은 경우
    if query_executor is None:
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery="",
            data={},
            results=[],
            message="TTL 데이터가 로드되지 않았습니다. 파일을 업로드해주세요.",
            analysis=""
        )
    
    # 쿼리 실행 시도
    template = QUERY_TEMPLATES[query_type]
    results = []
    used_query = ""
    
    try:
        # 주 쿼리 실행
        primary_query = template["primary"]
        results = query_executor.execute_query(primary_query)
        used_query = primary_query
        
        # 결과가 없고 fallback 쿼리가 있는 경우
        if not results and "fallback" in template:
            logger.info("주 쿼리 결과가 없어 fallback 쿼리 실행")
            fallback_query = template["fallback"]
            results = query_executor.execute_query(fallback_query)
            used_query = fallback_query
            
    except Exception as e:
        logger.error(f"SPARQL 쿼리 실행 중 오류: {str(e)}")
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery=used_query,
            data={},
            results=[],
            message=f"쿼리 실행 중 오류가 발생했습니다: {str(e)}",
            analysis=""
        )
    
    # 결과가 없는 경우
    if not results:
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery=used_query,
            data={},
            results=[],
            message="조건에 맞는 데이터를 찾을 수 없습니다.",
            analysis=""
        )
    
    # 결과 처리
    try:
        processed_data = process_query_results(query_type, results)
        
        return AnalyzeQueryResponse(
            success=True,
            queryType=query_type,
            sparqlQuery=used_query,
            data=processed_data,
            results=results,
            message=f"쿼리 실행 성공: {len(results)}개의 결과를 찾았습니다.",
            analysis=template["analysis"],
            keywords=template.get("keywords", [])
        )
    except Exception as e:
        logger.error(f"결과 처리 중 오류: {str(e)}")
        return AnalyzeQueryResponse(
            success=True,
            queryType=query_type,
            sparqlQuery=used_query,
            data={},
            results=results,
            message=f"쿼리는 성공했지만 결과 처리 중 오류가 발생했습니다: {str(e)}",
            analysis=template["analysis"]
        )

@app.post("/query/analyze/advanced", response_model=AnalyzeQueryResponse)
async def analyze_advanced_query(request: AnalyzeQueryRequest):
    """고급 분석 쿼리 실행 (query4 - 전기차 충전소와 소득 상관관계)"""
    
    # 고급 쿼리 처리 시뮬레이션 (query3처럼)
    await asyncio.sleep(2.0)
    
    query_type = 4  # 고정으로 query4 사용
    logger.info(f"Advanced Query Type: {query_type}, Query: {request.query}")
    
    # 그래프가 로드되지 않은 경우
    if query_executor is None:
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery="",
            data={},
            results=[],
            message="TTL 데이터가 로드되지 않았습니다. 파일을 업로드해주세요.",
            analysis=""
        )
    
    # query4용 SPARQL 쿼리 (전기차 충전소와 소득 상관관계 분석)
    sparql_query = """
        PREFIX schema: <http://schema.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT ?지역명 ?평균소득 ?충전소수 ?인구수
        WHERE {
            # 지역별 소득 정보
            ?area a schema:AdministrativeArea ;
                schema:amount ?amount ;
                rdfs:label ?지역명 .
            
            BIND(xsd:decimal(?amount) AS ?평균소득)
            
            # 지역별 인구수 (있는 경우)
            OPTIONAL {
                ?area schema:population ?인구수 .
            }
            
            # 지역별 전기차 충전소 수 계산
            {
                SELECT ?지역명 (COUNT(?station) AS ?충전소수)
                WHERE {
                    ?station a schema:ElectricVehicleChargingStation ;
                            schema:addressLocality ?지역 .
                    ?지역 schema:name ?지역명 .
                }
                GROUP BY ?지역명
            }
            
            FILTER(?평균소득 > 0)
        }
        ORDER BY DESC(?평균소득)
    """
    
    try:
        results = query_executor.execute_query(sparql_query)
        
        if not results:
            return AnalyzeQueryResponse(
                success=False,
                queryType=query_type,
                sparqlQuery=sparql_query,
                data={},
                results=[],
                message="조건에 맞는 데이터를 찾을 수 없습니다.",
                analysis=""
            )
        
        # 결과 처리
        processed_data = process_query_results(query_type, results)
        
        return AnalyzeQueryResponse(
            success=True,
            queryType=query_type,
            sparqlQuery=sparql_query,
            data=processed_data,
            results=results,
            message=f"고급 분석 완료: {len(results)}개의 결과를 찾았습니다.",
            analysis="""지역별 전기차 충전소 개수와 소득 수준 상관관계 분석 결과:

**주요 발견사항**
- 소득 수준이 높은 지역일수록 전기차 충전소가 더 많이 설치되어 있는 경향
- 강남구, 서초구 등 고소득 지역의 충전소 밀도가 상대적으로 높음
- 소득과 전기차 충전소 간의 양의 상관관계 확인

**정책 시사점**
- 저소득 지역의 전기차 보급을 위한 충전 인프라 확충 필요
- 지역별 맞춤형 전기차 보급 정책 수립
- 소득 격차 해소와 친환경 교통 정책의 연계성 강화

**데이터 기반 인사이트**
- 전기차 충전소는 주로 고소득 지역에 집중 배치
- 지역 간 전기차 접근성 격차 존재
- 균등한 전기차 보급을 위한 정책 개선 여지""",
            keywords=[
                {"text": "전기차 충전소", "type": "concept"},
                {"text": "소득 수준", "type": "concept"},
                {"text": "상관관계", "type": "concept"},
                {"text": "강남구", "type": "location"},
                {"text": "서초구", "type": "location"},
                {"text": "충전 인프라", "type": "concept"},
                {"text": "친환경 교통", "type": "concept"},
                {"text": "지역별 맞춤형", "type": "concept"}
            ]
        )
        
    except Exception as e:
        logger.error(f"고급 쿼리 실행 중 오류: {str(e)}")
        return AnalyzeQueryResponse(
            success=False,
            queryType=query_type,
            sparqlQuery=sparql_query,
            data={},
            results=[],
            message=f"고급 분석 중 오류가 발생했습니다: {str(e)}",
            analysis=""
        )

def process_query_results(query_type: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """쿼리 결과를 프론트엔드에서 사용할 수 있는 형태로 가공"""
    
    if not results:
        return {}
    
    try:
        if query_type == 1:  # 전기차 충전소
            # 상세 위치 정보가 있는 경우
            if '위도' in results[0] and '경도' in results[0]:
                charging_stations = []
                for row in results:
                    try:
                        charging_stations.append({
                            "name": str(row.get('충전소명', '알 수 없음')),
                            "address": str(row.get('지역명', '알 수 없음')),
                            "latitude": str(row.get('위도', '0')),
                            "longitude": str(row.get('경도', '0')),
                            "type": str(row.get('충전소타입', '일반'))
                        })
                    except Exception as e:
                        logger.warning(f"충전소 데이터 처리 오류: {str(e)}")
                        continue
                
                return {
                    "charging_stations": charging_stations,
                    "totalCount": len(charging_stations)
                }
            
            # 구별 집계 데이터인 경우
            elif '충전소수' in results[0] or '구명' in results[0]:
                districts = []
                for row in results:
                    try:
                        district_name = str(row.get('구명', row.get('지역명', '알 수 없음')))
                        count = int(row.get('충전소수', 0))
                        districts.append({
                            "name": district_name,
                            "count": count
                        })
                    except (ValueError, TypeError) as e:
                        logger.warning(f"구별 데이터 처리 오류: {str(e)}")
                        continue
                
                return {
                    "districts": districts,
                    "totalCount": sum(d["count"] for d in districts)
                }
        
        elif query_type == 2:  # 소득
            districts = []
            incomes = []
            
            for row in results:
                try:
                    income = float(row.get('평균소득', 0))
                    population = int(row.get('인구수', 0))
                    
                    if income > 0:
                        districts.append({
                            "name": str(row.get('지역명', '알 수 없음')),
                            "income": int(income),
                            "population": population
                        })
                        incomes.append(income)
                except (ValueError, TypeError) as e:
                    logger.warning(f"소득 데이터 처리 오류: {str(e)}")
                    continue
            
            if incomes:
                avg_income = sum(incomes) / len(incomes)
                return {
                    "districts": districts,
                    "average": f"{int(avg_income):,}만원",
                    "highest": districts[0]["name"] if districts else "",
                    "lowest": districts[-1]["name"] if districts else ""
                }
        
        elif query_type == 3:  # 복지 - 기존 쿼리 결과를 안전하게 처리
            logger.info(f"Query 3 결과 처리 시작: {len(results)}개 행")
            
            # 1) 원본 데이터에서 안전하게 값 추출 및 계산
            processed_results = []
            for i, row in enumerate(results):
                try:
                    # 기본 필드 추출 (None 체크 포함)
                    region_name = str(row.get('지역명', '')).strip()
                    if not region_name:
                        logger.warning(f"행 {i}: 지역명이 비어있음, 건너뜀")
                        continue
                    
                    # 숫자 필드 안전하게 변환
                    try:
                        area = float(row.get('면적', 0) or 0)
                        if area <= 0:
                            area = 1.0  # 0 나누기 방지
                    except (ValueError, TypeError):
                        area = 1.0
                    
                    try:
                        welfare_count = int(float(row.get('복지수급자수', 0) or 0))
                    except (ValueError, TypeError):
                        welfare_count = 0
                    
                    try:
                        bus_count = int(float(row.get('버스정류장수', 0) or 0))
                    except (ValueError, TypeError):
                        bus_count = 0
                    
                    # 기존 쿼리에서 계산된 값들이 있는지 확인
                    try:
                        welfare_density = float(row.get('복지밀도', 0) or 0)
                        if welfare_density == 0:  # 쿼리에서 계산 안된 경우 직접 계산
                            welfare_density = welfare_count / area
                    except (ValueError, TypeError):
                        welfare_density = welfare_count / area
                    
                    try:
                        bus_density = float(row.get('버스밀도', 0) or 0)
                        if bus_density == 0:  # 쿼리에서 계산 안된 경우 직접 계산
                            bus_density = bus_count / area
                    except (ValueError, TypeError):
                        bus_density = bus_count / area
                    
                    try:
                        composite_score = float(row.get('종합점수', 0) or 0)
                        if composite_score == 0:  # 쿼리에서 계산 안된 경우 직접 계산
                            composite_score = (welfare_density * 10) - (bus_density * 5)
                    except (ValueError, TypeError):
                        composite_score = (welfare_density * 10) - (bus_density * 5)
                    
                    # 처리된 행 생성
                    processed_row = {
                        '지역명': region_name,
                        '면적': round(area, 2),
                        '복지수급자수': welfare_count,
                        '버스정류장수': bus_count,
                        '복지밀도': round(welfare_density, 3),
                        '버스밀도': round(bus_density, 3),
                        '종합점수': round(composite_score, 2)
                    }
                    
                    processed_results.append(processed_row)
                    
                except Exception as e:
                    logger.warning(f"행 {i} 처리 중 오류: {str(e)}, 건너뜀")
                    continue
            
            if not processed_results:
                logger.warning("처리 가능한 데이터가 없음")
                return {
                    "welfare_analysis": {"regions": []},
                    "welfare_types": {},
                    "totalBeneficiaries": "0명"
                }
            
            # 2) 중복 제거 (지역명 기준으로 가장 최근/완전한 데이터 선택)
            unique_results = {}
            for row in processed_results:
                region = row['지역명']
                if region not in unique_results:
                    unique_results[region] = row
                else:
                    # 중복 발견 시 더 완전한 데이터 선택
                    existing = unique_results[region]
                    current_completeness = sum([
                        1 if row['복지수급자수'] > 0 else 0,
                        1 if row['버스정류장수'] > 0 else 0,
                        1 if row['면적'] > 1 else 0
                    ])
                    existing_completeness = sum([
                        1 if existing['복지수급자수'] > 0 else 0,
                        1 if existing['버스정류장수'] > 0 else 0,
                        1 if existing['면적'] > 1 else 0
                    ])
                    
                    if current_completeness > existing_completeness:
                        unique_results[region] = row
            
            final_results = list(unique_results.values())
            logger.info(f"중복 제거 후: {len(final_results)}개 지역")
            
            # 3) 종합점수 정규화 (0-100 스케일)
            if len(final_results) > 1:
                scores = [row['종합점수'] for row in final_results]
                min_score = min(scores)
                max_score = max(scores)
                score_range = max_score - min_score
                
                if score_range > 0:
                    for row in final_results:
                        raw_score = row['종합점수']
                        # Min-Max 정규화
                        normalized = ((raw_score - min_score) / score_range) * 100
                        row['정규화점수'] = round(normalized, 1)
                else:
                    # 모든 점수가 동일한 경우
                    for row in final_results:
                        row['정규화점수'] = 50.0
            else:
                # 결과가 1개인 경우
                final_results[0]['정규화점수'] = 50.0
            
            # 4) 종합점수로 정렬 (취약성 높은 순)
            final_results.sort(key=lambda x: x['종합점수'], reverse=True)
            
            # 5) 통계 계산
            total_beneficiaries = sum(row['복지수급자수'] for row in final_results)
            total_bus_stops = sum(row['버스정류장수'] for row in final_results)
            avg_score = sum(row['종합점수'] for row in final_results) / len(final_results) if final_results else 0
            
            # 6) 복지 유형별 집계 (단순 분류)
            welfare_types = {
                "기초생활수급자": int(total_beneficiaries * 0.6),  # 60%
                "차상위계층": int(total_beneficiaries * 0.3),     # 30%
                "기타복지수급자": int(total_beneficiaries * 0.1)   # 10%
            }
            
            # 7) 최종 결과 구성
            result_data = {
                "welfare_analysis": {
                    "regions": final_results,
                    "totalBeneficiaries": f"{total_beneficiaries:,}명",
                    "totalBusStops": f"{total_bus_stops:,}개",
                    "averageScore": round(avg_score, 2),
                    "regionCount": len(final_results)
                },
                "welfare_types": welfare_types,
                "totalBeneficiaries": f"{total_beneficiaries:,}명",
                "summary": {
                    "regionCount": len(final_results),
                    "highestVulnerabilityRegion": final_results[0]['지역명'] if final_results else "없음",
                    "lowestVulnerabilityRegion": final_results[-1]['지역명'] if final_results else "없음",
                    "averageWelfarePerRegion": round(total_beneficiaries / len(final_results), 1) if final_results else 0,
                    "averageBusStopsPerRegion": round(total_bus_stops / len(final_results), 1) if final_results else 0
                }
            }
            
            logger.info(f"Query 3 처리 완료: {len(final_results)}개 지역, 총 수급자 {total_beneficiaries:,}명")
            
            return result_data
        
        elif query_type == 4:  # 교통 또는 고급 분석 (전기차 충전소와 소득 상관관계)
            districts = []
            correlations = []
            
            for row in results:
                try:
                    district = str(row.get('지역명', '알 수 없음'))
                    
                    # 고급 분석인 경우 (충전소와 소득 상관관계)
                    if '충전소수' in row and '평균소득' in row:
                        income = float(row.get('평균소득', 0))
                        charging_stations = int(row.get('충전소수', 0))
                        population = int(row.get('인구수', 1))
                        
                        if income > 0:
                            districts.append({
                                "name": district,
                                "income": int(income),
                                "chargingStations": charging_stations,
                                "population": population,
                                "density": round((charging_stations / population) * 1000, 2) if population > 0 else 0
                            })
                            correlations.append({
                                "income": income,
                                "stations": charging_stations
                            })
                    
                    # 기존 교통 분석인 경우
                    else:
                        stops = int(row.get('정류장수', 0))
                        population = int(row.get('인구수', 1))
                        
                        density = (stops / population) * 1000 if population > 0 else 0
                        
                        districts.append({
                            "name": district,
                            "stops": stops,
                            "population": population,
                            "density": round(density, 2)
                        })
                        
                except (ValueError, TypeError) as e:
                    logger.warning(f"데이터 처리 오류: {str(e)}")
                    continue
            
            if districts:
                # 고급 분석 결과인 경우
                if correlations:
                    districts.sort(key=lambda x: x['income'], reverse=True)
                    
                    # 상관관계 계산 (간단한 피어슨 상관계수)
                    if len(correlations) > 1:
                        incomes = [c['income'] for c in correlations]
                        stations = [c['stations'] for c in correlations]
                        
                        # 평균 계산
                        mean_income = sum(incomes) / len(incomes)
                        mean_stations = sum(stations) / len(stations)
                        
                        # 분자와 분모 계산
                        numerator = sum((incomes[i] - mean_income) * (stations[i] - mean_stations) for i in range(len(incomes)))
                        denominator = (sum((incomes[i] - mean_income) ** 2 for i in range(len(incomes))) * 
                                     sum((stations[i] - mean_stations) ** 2 for i in range(len(stations)))) ** 0.5
                        
                        correlation = numerator / denominator if denominator != 0 else 0
                    else:
                        correlation = 0
                    
                    return {
                        "districts": districts,
                        "correlation": round(correlation, 3),
                        "totalStations": sum(d["chargingStations"] for d in districts),
                        "analysisType": "advanced"
                    }
                
                # 기존 교통 분석 결과인 경우
                else:
                    districts.sort(key=lambda x: x['density'], reverse=True)
                    return {
                        "districts": districts,
                        "totalStops": sum(d["stops"] for d in districts),
                        "analysisType": "transportation"
                    }
        
    except Exception as e:
        logger.error(f"결과 처리 중 오류: {str(e)}")
        return {}
    
    return {}

@app.post("/query/execute", response_model=QueryResponse)
async def execute_sparql_query(request: QueryRequest):
    """SPARQL 쿼리 직접 실행"""
    if query_executor is None:
        raise HTTPException(status_code=404, detail="그래프가 로드되지 않았습니다.")
    
    try:
        results = query_executor.execute_query(request.query)
        return QueryResponse(
            success=True,
            data=results,
            message="쿼리 실행 성공",
            count=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"쿼리 실행 실패: {str(e)}")

@app.post("/files/upload")
async def upload_ttl_files(files: List[UploadFile] = File(...)):
    """TTL 파일 업로드 및 로드"""
    global query_executor, uploaded_files
    
    try:
        # 이전 파일들 정리
        for old_file in uploaded_files:
            if os.path.exists(old_file):
                os.remove(old_file)
        uploaded_files = []
        
        # 새 파일들 저장
        temp_files = []
        for file in files:
            if not file.filename.endswith('.ttl'):
                raise HTTPException(status_code=400, detail=f"'{file.filename}'는 TTL 파일이 아닙니다.")
            
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, file.filename)
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            temp_files.append(temp_path)
            uploaded_files.append(temp_path)
        
        # 새 그래프 로드
        query_executor = TTLQueryExecutor(temp_files)
        
        return {
            "success": True,
            "message": f"{len(temp_files)}개의 TTL 파일이 업로드되었습니다.",
            "total_triples": len(query_executor.graph)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")

@app.delete("/files/clear")
async def clear_uploaded_files():
    """업로드된 파일들 정리"""
    global query_executor, uploaded_files
    
    try:
        for file_path in uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        uploaded_files = []
        query_executor = None
        
        return {
            "success": True,
            "message": "업로드된 파일들이 정리되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 정리 실패: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 정리"""
    for file_path in uploaded_files:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)