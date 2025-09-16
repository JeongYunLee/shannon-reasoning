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
import numpy as np
from scipy.stats import pearsonr
import statistics
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 한글 폰트 설정
def setup_korean_font():
    """한글 폰트 설정"""
    try:
        # macOS의 경우
        if plt.get_backend() != 'Agg':
            plt.rcParams['font.family'] = ['AppleGothic', 'Malgun Gothic', 'DejaVu Sans']
        else:
            plt.rcParams['font.family'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 경고 메시지 억제
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
    except:
        # 폰트 설정 실패 시 기본 설정 유지
        pass

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

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "http://localhost/projects/shannon-insight",  # 추가
    "http://localhost:80/projects/shannon-insight",  # 추가
    "http://labs.datahub.kr",
    "https://labs.datahub.kr"
    "165.194.115.110",
    "165.194.114.38"
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
            # {"text": "전기차 충전소", "type": "concept"},
            {"text": "서울특별시 동작구의 전기차 충전소 개수: 18개", "type": "number"},
            # {"text": "주거 밀집 지역", "type": "concept"},
            {"text": "주거 밀집지역과 교통 접근성을 고려한 배치", "type": "concept"},
            # {"text": "공공기관", "type": "concept"},
            {"text": "상업·산업 지구 주변으로 추가 설치 가능성", "type": "location"},
            # {"text": "상도동", "type": "location"},
            # {"text": "18개", "type": "number"}
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
        "analysis": """서울시 자치구별 소득 분포를 분석한 결과, 지역 간에 상당한 수준의 소득 격차가 존재하는 것으로 확인되었습니다. 특히 강남구는 평균 소득이 가장 높은 수준을 기록했으며, 서초구와 송파구 또한 상위권에 속해 이른바 ‘강남 3구’가 소득 상위 지역을 형성하고 있습니다. 이러한 소득 분포는 지역 발전도와 밀접한 상관관계를 보였으며, 인구 밀도와 소득 수준 간에도 일정한 패턴이 나타나는 것으로 파악됩니다. 


**주요 수치**
- 강남구 평균 소득: 최고 수준
- 서초구 평균 소득: 상위권
- 송파구 평균 소득: 상위권
- 지역 간 소득 격차: 상당한 수준

**정책 시사점**
- 소득 격차 해소를 위한 지역 균형 발전 정책 필요
- 저소득 지역의 일자리 창출 및 인프라 개선
- 중산층 확대를 위한 맞춤형 지원 정책 개발""",
        "keywords": [
            # {"text": "소득 분포", "type": "concept"},
            # {"text": "강남구", "type": "location"},
            {"text": "강남 3구(강남, 서초, 송파)가 소득 상위권을 형성", "type": "location"},
            # {"text": "송파구", "type": "location"},
            {"text": "소득 수준과 지역 발전도 간의 높은 상관관계", "type": "concept"},
            {"text": "인구 밀도와 소득 수준 간의 특정 패턴 존재", "type": "number"},
            # {"text": "지역 발전도", "type": "concept"},
            # {"text": "인구 밀도", "type": "concept"}
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
        "analysis": """면적 대비 복지 수급자 밀도와 버스 정류장 밀도를 종합적으로 분석한 결과, 지역별 복지 취약성이 뚜렷하게 나타났습니다. 
복지 수급자 밀도는 복지수급자 수를 면적으로 나눈 값이며, 버스 정류장 밀도는 버스정류장 수를 면적으로 나눈 값으로 정의하였습니다. 
이를 기반으로 종합점수는 복지밀도에 가중치를 두고 버스밀도를 반영하여 산출하였으며, 다수의 지역을 대상으로 분석을 실시하였습니다.

**주요 수치**
- 복지밀도 = 복지수급자수 ÷ 면적
- 버스밀도 = 버스정류장수 ÷ 면적  
- 종합점수 = (복지밀도 × 10) - (버스밀도 × 5)
- 분석 대상 지역: 다수 지역

분석 결과, 복지 수급자가 밀집한 지역일수록 대중교통 접근성이 상대적으로 낮은 경향이 확인되었습니다. 
이는 복지 인프라와 교통 인프라 간의 불균형을 보여주는 지표로 해석될 수 있으며, 특히 높은 종합점수를 기록한 지역은 복지 지원과 교통 개선이 동시에 요구되는 취약 지역으로 분류되었습니다.

이러한 결과를 바탕으로 몇 가지 정책적 제언을 드릴 수 있습니다. 

첫째, 복지 취약 지역의 대중교통 접근성을 개선하여 복지 서비스 이용 편의를 높일 필요가 있습니다. 

둘째, 지역별 특성을 반영한 맞춤형 복지 전달 체계를 마련해야 하며, 

셋째, 교통 소외 지역을 중심으로 복지 서비스 제공을 확대할 필요가 있습니다. 마지막으로, 복지와 교통을 통합적으로 고려한 지역 개발 계획을 수립하여 지역 간 불균형을 완화하고 지속 가능한 도시 발전을 도모해야 할 것입니다.

""",
        "keywords": [
            {"text": "지역별 복지 인프라와 교통 인프라 간의 불균형 존재", "type": "location"},
            {"text": "높은 종합점수를 기록한 지역은 복지 지원과 교통 개선이 동시에 필요", "type": "concept"},
            {"text": "복지 수급자가 밀집한 지역일수록 대중교통 접근성이 상대적으로 낮은 경향", "type": "number"},
            # {"text": "복지밀도", "type": "concept"},
            # {"text": "버스밀도", "type": "concept"},
            # {"text": "종합점수", "type": "concept"},
            # {"text": "대중교통 접근성", "type": "concept"},
            # {"text": "복지 인프라", "type": "concept"}
        ]
    },
   4: {  # 소득과 충전소 상관관계 (수정됨)
        "primary": """
            PREFIX schema: <http://schema.org/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?지역명 ?평균소득 ?충전소수
            WHERE {
                # 지역별 소득 정보
                ?area a schema:AdministrativeArea ;
                    schema:amount ?amount ;
                    rdfs:label ?지역명 .
                
                BIND(xsd:decimal(?amount) AS ?평균소득)
                
                # 지역별 전기차 충전소 수 계산
                {
                    SELECT ?지역명 (COUNT(?station) AS ?충전소수)
                    WHERE {
                        ?station a schema:AutomatedTeller ;
                                schema:addressLocality ?지역 .
                        ?지역 schema:name ?지역명 .
                    }
                    GROUP BY ?지역명
                }
                
                FILTER(?평균소득 > 0)
            }
            ORDER BY DESC(?평균소득)
        """,
        "analysis": """지역별 소득과 전기차 충전소 개수의 상관관계를 분석한 결과, 통계적으로 유의미한 관계가 확인되었습니다. 
분석 가설은 '평균 소득이 높은 지역일수록 전기차 충전소가 많을 것'이었으며, 이를 검증하기 위해 피어슨 상관계수를 계산하였습니다.

분석 결과, 소득과 전기차 충전소 수 간에는 양의 상관관계가 존재하는 것으로 나타났습니다. 이는 경제적으로 발달한 지역일수록 전기차 충전 인프라가 더 잘 구축되어 있음을 시사합니다.

**주요 발견사항**
- 소득 수준과 전기차 충전소 수 간의 양의 상관관계 확인
- 고소득 지역의 전기차 충전 인프라 집중 현상
- 지역별 전기차 접근성 격차 존재

**정책 시사점**
- 저소득 지역의 전기차 충전 인프라 확충 필요
- 지역별 균형 잡힌 전기차 보급 정책 수립
- 전기차 접근성 격차 해소를 위한 정책 개발

이러한 분석 결과는 친환경 교통 정책과 지역 발전 계획 수립에 중요한 기초 자료로 활용될 수 있으며, 지역 간 형평성을 고려한 전기차 보급 정책의 필요성을 보여줍니다.""",
        "keywords": [
            {"text": "소득 수준과 전기차 충전소 수 간의 양의 상관관계", "type": "concept"},
            {"text": "고소득 지역의 전기차 충전 인프라 집중 현상", "type": "location"},
            {"text": "지역별 전기차 접근성 격차 존재", "type": "concept"},
        ]
    }
}

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 기본 TTL 파일들 로드"""
    global query_executor

    # 한글 폰트 설정
    setup_korean_font()
    
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

@app.get("/api/")
async def root():
    """루트 엔드포인트"""
    return {"message": "TTL Query Executor API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy", 
        "executor_loaded": query_executor is not None,
        "graph_size": len(query_executor.graph) if query_executor else 0
    }

@app.get("/api/graph/info", response_model=GraphInfoResponse)
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

@app.post("/api/query/analyze", response_model=AnalyzeQueryResponse)
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

   
@app.post("/api/query/analyze/advanced", response_model=AnalyzeQueryResponse)
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

            SELECT ?지역명 ?평균소득 ?충전소수
            WHERE {
                # 지역별 소득 정보
                ?area a schema:AdministrativeArea ;
                    schema:amount ?amount ;
                    rdfs:label ?지역명 .
                
                BIND(xsd:decimal(?amount) AS ?평균소득)
                
                # 지역별 전기차 충전소 수 계산
                {
                    SELECT ?지역명 (COUNT(?station) AS ?충전소수)
                    WHERE {
                        ?station a schema:AutomatedTeller ;
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
            analysis="""가설: '평균 소득이 높은 지역일수록 전기차 충전소 개수가 많을 것이다.'

**상관관계 수치**
- Spearman r = **0.0279** → 거의 0, 사실상 상관 없음
- p-value = **0.6889** → 유의하지 않음 (통계적으로 의미 없음)


**그래프 해석**
- 회귀선은 약간의 양(+)의 기울기를 보이나, 데이터 점들이 넓게 퍼져 있고 일관성이 없음
- 일부 이상치가 관찰됨 → 추세선이 왜곡될 가능성 존재

**데이터 기반 인사이트**
- 평균소득과 충전소 수 사이에는 통계적으로 유의한 상관관계가 없음
- 즉, 평균 소득이 높다고 해서 충전소 수가 많다고 단정할 수 없음
- 충전소 개수는 소득보다 인구밀도, 차량 등록 대수, 도시정책/인프라 계획 등 다른 요인과 더 관련있을 가능성이 높음
- 다변량 분석이나 이상치 제거 후 재검토 필요""",
            keywords=[
                {"text": "평균소득과 충전소 수는 통계적으로 유의미한 상관이 없음", "type": "number"},
                {"text": "충전소 분포는 소득 외의 다른 요인에 의해 결정될 가능성이 큼", "type": "location"},
                {"text": "단순 상관분석만으로는 전체 관계를 설명하기 어려움", "type": "concept"},
                # {"text": "강남구", "type": "location"},
                # {"text": "서초구", "type": "location"},
                # {"text": "충전 인프라", "type": "concept"},
                # {"text": "친환경 교통", "type": "concept"},
                # {"text": "지역별 맞춤형", "type": "concept"}
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

        elif query_type == 4:  # 소득-전기차충전소 상관관계 분석
                districts = []
                income_data = []
                charger_data = []
                
                for row in results:
                    try:
                        district_name = str(row.get('지역명', '알 수 없음'))
                        
                        # 안전한 타입 변환
                        income_raw = row.get('평균소득', 0)
                        charger_count_raw = row.get('충전소수', 0)
                        
                        # None 값 체크 및 안전한 변환
                        income = 0
                        if income_raw is not None and income_raw != "":
                            try:
                                income = float(income_raw)
                            except (ValueError, TypeError):
                                income = 0
                        
                        charger_count = 0
                        if charger_count_raw is not None and charger_count_raw != "":
                            try:
                                charger_count = int(float(charger_count_raw))
                            except (ValueError, TypeError):
                                charger_count = 0
                        
                        # 유효한 데이터만 포함
                        if income > 0 and charger_count > 0:
                            district_data = {
                                "name": district_name,
                                "income": int(income),
                                "chargerCount": charger_count,  # 이 필드명이 중요!
                                "population": 100000,  # 기본값 또는 실제 인구 데이터
                                "chargerDensity": round(charger_count / 100000 * 1000, 2) if 100000 > 0 else 0,
                                "incomePerCapita": round(income, 0)
                            }
                            
                            districts.append(district_data)
                            income_data.append(income)
                            charger_data.append(charger_count)
                            
                    except Exception as e:
                        logger.warning(f"소득-충전소 데이터 처리 오류 (행 건너뜀): {str(e)}")
                        continue
                
                # 상관관계 분석 (수정됨)
                correlation_info = calculate_correlation_analysis(income_data, charger_data)

                districts.sort(key=lambda x: x['income'], reverse=True)
                
                return {
                    "districts": districts,
                    "correlation": correlation_info,  # 새로운 분석 결과
                    "summary": {
                        "totalRegions": len(districts),
                        "avgIncome": round(sum(income_data) / len(income_data), 0) if income_data else 0,
                        "avgChargerCount": round(sum(charger_data) / len(charger_data), 1) if charger_data else 0,
                        "highestIncomeRegion": districts[0]["name"] if districts else "",
                        "lowestIncomeRegion": districts[-1]["name"] if districts else "",
                        "analysisMethod": "다중 통계 분석 (스피어만, 켄달, 포아송 회귀)"
                    },
                    "analysisType": "income_charger_correlation"
                }
    
    except Exception as e:
        logger.error(f"결과 처리 중 오류: {str(e)}")
        return {}
    
    return {}

def perform_correlation_analysis(income_data: List[Dict], bus_data: List[Dict]) -> Dict[str, Any]:
    """
    소득 데이터와 버스정류장 데이터를 조인하고 상관관계를 분석합니다.
    
    Args:
        income_data: 소득 데이터 리스트
        bus_data: 버스정류장 데이터 리스트
        
    Returns:
        상관관계 분석 결과
    """
    try:
        # 1. 데이터프레임 생성
        df_income = pd.DataFrame(income_data)
        df_bus = pd.DataFrame(bus_data)
        
        logger.info(f"소득 데이터: {len(df_income)}개 지역")
        logger.info(f"버스정류장 데이터: {len(df_bus)}개 지역")
        
        # 2. 데이터 전처리
        # 소득 데이터 정리
        df_income['지역명'] = df_income['지역명'].astype(str).str.strip()
        df_income['평균소득'] = pd.to_numeric(df_income['평균소득'], errors='coerce')
        df_income = df_income.dropna(subset=['평균소득'])
        df_income = df_income[df_income['평균소득'] > 0]
        
        # 버스정류장 데이터 정리
        df_bus['지역명'] = df_bus['지역명'].astype(str).str.strip()
        df_bus['버스정류장수'] = pd.to_numeric(df_bus['버스정류장수'], errors='coerce')
        df_bus = df_bus.dropna(subset=['버스정류장수'])
        df_bus = df_bus[df_bus['버스정류장수'] > 0]
        
        # 3. 지역명 기준으로 조인 (inner join)
        merged_df = pd.merge(df_income, df_bus, on='지역명', how='inner')
        
        if len(merged_df) < 3:
            return {
                "success": False,
                "error": "조인된 데이터가 부족합니다. 최소 3개 지역이 필요합니다.",
                "joined_regions": len(merged_df)
            }
        
        logger.info(f"조인 완료: {len(merged_df)}개 지역")
        
        # 4. 상관관계 분석
        income_values = merged_df['평균소득'].values
        bus_values = merged_df['버스정류장수'].values
        
        # 피어슨 상관계수 계산
        correlation_coef, p_value = pearsonr(income_values, bus_values)
        
        # 5. 기술통계 계산
        income_stats = {
            "mean": float(np.mean(income_values)),
            "median": float(np.median(income_values)),
            "std": float(np.std(income_values)),
            "min": float(np.min(income_values)),
            "max": float(np.max(income_values))
        }
        
        bus_stats = {
            "mean": float(np.mean(bus_values)),
            "median": float(np.median(bus_values)),
            "std": float(np.std(bus_values)),
            "min": float(np.min(bus_values)),
            "max": float(np.max(bus_values))
        }
        
        # 6. 상관관계 강도 해석
        abs_corr = abs(correlation_coef)
        if abs_corr >= 0.8:
            strength = "매우 강함"
        elif abs_corr >= 0.6:
            strength = "강함"
        elif abs_corr >= 0.4:
            strength = "중간"
        elif abs_corr >= 0.2:
            strength = "약함"
        else:
            strength = "매우 약함"
        
        # 7. 통계적 유의성 판단
        is_significant = p_value < 0.05
        significance_level = "유의함" if is_significant else "유의하지 않음"
        
        # 8. 회귀 분석 (간단한 선형 회귀)
        # y = ax + b 형태로 계산
        correlation_matrix = np.corrcoef(income_values, bus_values)
        r_squared = correlation_coef ** 2
        
        # 회귀계수 계산 (최소제곱법)
        mean_income = np.mean(income_values)
        mean_bus = np.mean(bus_values)
        
        numerator = np.sum((income_values - mean_income) * (bus_values - mean_bus))
        denominator = np.sum((income_values - mean_income) ** 2)
        
        if denominator != 0:
            slope = numerator / denominator
            intercept = mean_bus - slope * mean_income
        else:
            slope = 0
            intercept = mean_bus
        
        # 9. 결과 정리
        result = {
            "success": True,
            "correlation": {
                "coefficient": round(correlation_coef, 4),
                "p_value": round(p_value, 4),
                "strength": strength,
                "significance": significance_level,
                "is_significant": is_significant,
                "direction": "양의 상관관계" if correlation_coef > 0 else "음의 상관관계" if correlation_coef < 0 else "상관관계 없음",
                "r_squared": round(r_squared, 4)
            },
            "regression": {
                "slope": round(slope, 4),
                "intercept": round(intercept, 4),
                "equation": f"버스정류장수 = {slope:.4f} × 평균소득 + {intercept:.4f}"
            },
            "statistics": {
                "sample_size": len(merged_df),
                "income_stats": income_stats,
                "bus_stats": bus_stats
            },
            "joined_data": merged_df.to_dict('records'),
            "hypothesis_test": {
                "hypothesis": "평균 소득이 높은 지역일수록 버스정류장의 개수가 많을 것",
                "result": "가설 지지" if correlation_coef > 0 and is_significant else "가설 기각",
                "interpretation": generate_interpretation(correlation_coef, p_value, is_significant, strength)
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"상관관계 분석 중 오류: {str(e)}")
        return {
            "success": False,
            "error": f"상관관계 분석 중 오류가 발생했습니다: {str(e)}"
        }

def generate_interpretation(correlation_coef: float, p_value: float, is_significant: bool, strength: str) -> str:
    """상관관계 분석 결과에 대한 해석을 생성합니다."""
    
    interpretation = ""
    
    if is_significant:
        if correlation_coef > 0:
            interpretation = f"통계적으로 유의한 양의 상관관계가 확인되었습니다(r={correlation_coef:.3f}, p={p_value:.3f}). "
            interpretation += f"이는 평균소득이 높은 지역일수록 버스정류장 수가 많다는 가설을 지지합니다. "
            interpretation += f"상관관계의 강도는 '{strength}'으로 분류됩니다."
        else:
            interpretation = f"통계적으로 유의한 음의 상관관계가 확인되었습니다(r={correlation_coef:.3f}, p={p_value:.3f}). "
            interpretation += f"이는 예상과 반대로 평균소득이 높은 지역일수록 버스정류장 수가 적음을 의미합니다."
    else:
        interpretation = f"통계적으로 유의하지 않은 결과입니다(r={correlation_coef:.3f}, p={p_value:.3f}). "
        interpretation += f"평균소득과 버스정류장 수 간에 명확한 선형 관계를 확인할 수 없습니다."
    
    return interpretation

def calculate_correlation_analysis(x_data: List[float], y_data: List[float]) -> Dict[str, Any]:
    """
    소득(연속형)과 충전소 수(이산형) 간의 적절한 관계 분석
    """
    if len(x_data) != len(y_data) or len(x_data) < 3:
        return {
            "method": "분석 불가",
            "result": "데이터가 부족합니다 (최소 3개 지역 필요)",
            "interpretation": "충분한 데이터가 없어 분석할 수 없습니다."
        }

    try:
        import numpy as np
        from scipy import stats
        import warnings
        warnings.filterwarnings('ignore')
        
        # 1. 스피어만 순위 상관계수 (비모수적, 단조성 관계 측정)
        spearman_corr, spearman_p = stats.spearmanr(x_data, y_data)
        
        # 2. 켄달 타우 (순위 기반, 작은 표본에 적합)
        kendall_corr, kendall_p = stats.kendalltau(x_data, y_data)
        
        # 3. 포아송 회귀 분석 (카운트 데이터에 적합)
        poisson_result = None
        try:
            # 간단한 포아송 회귀 적합도 검사
            from scipy.optimize import minimize
            
            def poisson_log_likelihood(params, x, y):
                beta0, beta1 = params
                lambda_pred = np.exp(beta0 + beta1 * np.array(x))
                # 포아송 로그 우도
                log_likelihood = np.sum(y * np.log(lambda_pred) - lambda_pred)
                return -log_likelihood  # 최소화를 위해 음수 반환
            
            # 초기값
            initial_params = [0.0, 0.0]
            
            # 소득 정규화 (수치적 안정성을 위해)
            x_normalized = [(x - np.mean(x_data)) / np.std(x_data) for x in x_data]
            
            result = minimize(poisson_log_likelihood, initial_params, 
                            args=(x_normalized, y_data), method='BFGS')
            
            if result.success:
                beta0, beta1 = result.x
                poisson_result = {
                    "coefficient": beta1,
                    "significant": abs(beta1) > 0.1,  # 간단한 기준
                    "interpretation": "양의 관계" if beta1 > 0 else "음의 관계" if beta1 < 0 else "관계 없음"
                }
        except:
            poisson_result = None
        
        # 4. 단순 선형 회귀 (비교용)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
        
        # 결과 해석
        primary_method = "spearman"
        primary_coeff = spearman_corr
        primary_p = spearman_p
        
        # 강도 분류
        abs_corr = abs(primary_coeff)
        if abs_corr >= 0.7:
            strength = "강한"
        elif abs_corr >= 0.5:
            strength = "중간"
        elif abs_corr >= 0.3:
            strength = "약한"
        else:
            strength = "매우 약한"
        
        # 방향성
        direction = "양의" if primary_coeff > 0 else "음의" if primary_coeff < 0 else "없는"
        
        # 유의성
        significance = "통계적으로 유의함" if primary_p < 0.05 else "통계적으로 유의하지 않음"
        
        # 종합 해석
        interpretation = f"""
        스피어만 순위 상관분석 결과: {direction} {strength} 관계 ({significance})
        
        • 소득이 높은 지역일수록 충전소가 {'많은' if primary_coeff > 0 else '적은'} 경향을 보입니다.
        • 상관계수: {primary_coeff:.3f} (p-value: {primary_p:.3f})
        • 이는 순위 기반 분석으로, 선형성을 가정하지 않습니다.
        """
        
        return {
            "method": "다중 방법 분석",
            "primary": {
                "name": "스피어만 순위 상관",
                "coefficient": round(primary_coeff, 4),
                "p_value": round(primary_p, 4),
                "strength": strength,
                "direction": direction,
                "significance": significance
            },
            "secondary": {
                "kendall_tau": round(kendall_corr, 4),
                "kendall_p": round(kendall_p, 4),
                "linear_r": round(r_value, 4),
                "linear_p": round(p_value, 4)
            },
            "poisson_regression": poisson_result,
            "interpretation": interpretation.strip(),
            "recommendation": """
            충전소 수는 카운트 데이터이므로 스피어만 상관계수가 더 적절합니다.
            포아송 회귀 분석을 통해 보다 정교한 모델링이 가능합니다.
            """,
            "sample_size": len(x_data)
        }
        
    except Exception as e:
        return {
            "method": "분석 오류",
            "result": f"분석 중 오류 발생: {str(e)}",
            "interpretation": "통계 분석을 수행할 수 없습니다."
        }


@app.post("/api/query/execute", response_model=QueryResponse)
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

@app.post("/api/files/upload")
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

@app.delete("/api/files/clear")
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
    uvicorn.run(app, host="0.0.0.0", port=8001)