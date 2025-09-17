<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-blue-50">
    <!-- Header -->
    <div class="bg-white/90 backdrop-blur-xl shadow-sm border-b border-gray-100/80">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3 cursor-pointer group" @click="refreshPage">
            <div class="relative">
              <div class="w-10 h-10 bg-gradient-to-br from-indigo-500/80 via-purple-600/80 to-blue-500/80 rounded-2xl flex items-center justify-center shadow-lg rotate-3 transform group-hover:rotate-0 transition-transform duration-300">
                <span class="text-white font-bold text-lg">S</span>
              </div>
              <div class="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent group-hover:from-indigo-600 group-hover:to-purple-600 transition-all duration-300">
                Shannon Insight
              </h1>
              <p class="text-sm text-gray-500 font-medium group-hover:text-gray-600 transition-colors duration-300">Advanced Data Intelligence Platform</p>
            </div>
          </div>
          <div class="hidden md:flex items-center space-x-2">
            <div class="px-3 py-1.5 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">
              Beta v1.0
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Hero Search Section -->
      <div class="relative overflow-hidden mb-8">
        <div class="absolute inset-0 bg-gradient-to-br from-slate-400/15 via-slate-500/15 to-slate-600/15 rounded-3xl transform rotate-1"></div>
        <!-- <div class="absolute inset-0 bg-gradient-to-br from-indigo-600/20 via-purple-600/20 to-pink-600/20 rounded-3xl transform rotate-1"></div> -->
        <!-- <div class="relative bg-gradient-to-br from-indigo-600 via-purple-700 to-pink-600 rounded-3xl p-6 lg:p-8 text-white shadow-2xl"> -->
          <div class="relative bg-gradient-to-br from-blue-900/70 to-purple-700/70 rounded-3xl p-6 lg:p-8 text-white shadow-2xl backdrop-blur-sm">
          <!-- Background Pattern -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute top-0 left-0 w-40 h-40 bg-white rounded-full -translate-x-20 -translate-y-20"></div>
            <div class="absolute bottom-0 right-0 w-32 h-32 bg-white rounded-full translate-x-16 translate-y-16"></div>
            <div class="absolute top-1/2 left-1/2 w-24 h-24 bg-white rounded-full -translate-x-12 -translate-y-12"></div>
          </div>
          
          <div class="relative z-10">
            <div class="text-center mb-6">
              <h2 class="text-xl lg:text-2xl font-semibold mb-3 leading-tight">
                데이터 속 숨겨진 
                <span class="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">인사이트</span>를 
                발견하세요
              </h2>
              <!-- <p class="text-lg text-white/90 font-medium">자연어 질문으로 복합적인 데이터 분석을 수행합니다</p> -->
            </div>
            
            <!-- Search Input -->
            <div class="max-w-2xl mx-auto mb-6">
              <div class="relative group">
                <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-white/10 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                <div class="relative flex items-center">
                  <div class="flex items-center flex-1 bg-white rounded-2xl shadow-xl overflow-hidden">
                    <svg class="w-5 h-5 text-gray-400 ml-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <input
                      v-model="userQuery"
                      placeholder="자연어로 질문을 입력하세요"
                      class="flex-1 px-4 py-4 text-gray-900 placeholder-gray-500 focus:outline-none text-base"
                      @keyup.enter="executeQuery"
                    />
                    <button
                      @click="executeQuery"
                      :disabled="loading || !userQuery.trim()"
                      class="m-2 flex items-center justify-center w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group"
                    >
                      <div v-if="loading" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
                      <svg v-else class="w-6 h-6 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m9 5 7 7-7 7"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Search Tags -->
            <div class="flex flex-wrap justify-center items-center gap-3 mb-8">
              <span class="text-white/80 text-sm font-medium">검색어 예시:</span>
              <button 
                v-for="(query, idx) in sampleQueries" 
                :key="idx"
                @click="loadSampleQuery(idx)"
                class="group flex items-center gap-2 px-3 py-2 bg-white/20 hover:bg-white/30 rounded-full text-xs font-medium transition-all duration-200 backdrop-blur-sm border border-white/20"
              >
                <!-- <span v-if="query.title === '전기차 충전소'">⚡</span> -->
                <!-- <span v-else-if="query.title === '소득 분포'">📊</span> -->
                <!-- <span v-else>🔄</span> -->
                <span>{{ query.title }}</span>
                <span class="text-xs px-1 py-0.5 rounded text-white/70 font-medium" 
                      :class="{
                        'bg-green-500/50': query.difficulty === 'basic',
                        'bg-red-500/50': query.difficulty === 'advanced'
                      }">
                  {{ query.difficulty === 'basic' ? 'basic' : 'advanced' }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis Tips Slider Section - First Screen Only -->
      <div v-if="!loading && !result" class="mb-12">
        <div class="relative overflow-hidden bg-white rounded-3xl shadow-sm border border-gray-100">
            <div class="px-6 py-4 border-b border-gray-100">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-600 flex">
                <span class="text-xl mr-2">💡</span>
                분석 팁
                </h3>
                <div class="flex space-x-1">
                <button
                    v-for="(tip, index) in analysisTips"
                    :key="index"
                    @click="currentTipIndex = index"
                    :class="[
                    'w-2 h-2 rounded-full transition-all duration-300',
                    currentTipIndex === index ? 'bg-indigo-500' : 'bg-gray-300'
                    ]"
                ></button>
                </div>
            </div>
            </div>
            
            <div class="relative h-56 overflow-hidden">
            <div 
                class="flex transition-transform duration-500 ease-in-out h-full"
                :style="{ transform: `translateX(-${currentTipIndex * 100}%)` }"
            >
                <div 
                v-for="(tip, index) in analysisTips" 
                :key="index"
                class="w-full flex-shrink-0 px-6 py-12 flex items-center justify-center"
                >
                <div class="text-center max-w-md">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-4 mx-auto shadow-lg">
                        <!-- 검색 아이콘 -->
                        <svg v-if="tip.icon === 'search'" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                        <!-- 차트 아이콘 -->
                        <svg v-else-if="tip.icon === 'chart'" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                        </svg>
                        <!-- 트렌드 아이콘 -->
                        <svg v-else-if="tip.icon === 'trend'" class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                        </svg>
                    </div>
                    <h4 class="font-bold text-gray-800 mb-2 text-lg text-center">{{ tip.title }}</h4>
                    <p class="text-sm text-gray-600 leading-relaxed mb-3 text-center">{{ tip.description }}</p>
                    <div class="text-xs text-gray-500 bg-gray-50 px-3 py-1 rounded-full inline-block">
                        {{ tip.example }}
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
      </div>

      <!-- Feature Boxes Section - First Screen Only -->
      <div v-if="!loading && !result" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="group relative overflow-hidden bg-white rounded-3xl shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-cyan-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative p-6 text-center">
            <div class="flex flex-col items-center mb-4">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-bold text-gray-800">복합추론</h3>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed mb-4">
              여러 데이터셋을 연결하여 복합적인 패턴과 인과관계 추론
            </p>
            <div class="flex items-center justify-center text-xs text-gray-500">
              <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
              고급 분석 기능
            </div>
          </div>
        </div>

        <div class="group relative overflow-hidden bg-white rounded-3xl shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-50 to-pink-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative p-6 text-center">
            <div class="flex flex-col items-center mb-4">
              <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
                </svg>
              </div>
              <h3 class="text-lg font-bold text-gray-800">다양한 데이터 소스</h3>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed mb-4">
              공공데이터, 통계청, 지자체 등 신뢰할 수 있는 데이터 총 1,698,462 트리플
            </p>
            <div class="flex items-center justify-center text-xs text-gray-500">
              <span class="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
              출처 제공
            </div>
          </div>
        </div>

        <div class="group relative overflow-hidden bg-white rounded-3xl shadow-lg border border-gray-100 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
          <div class="absolute inset-0 bg-gradient-to-br from-emerald-50 to-teal-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative p-6 text-center">
            <div class="flex flex-col items-center mb-4">
              <div class="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-bold text-gray-800">실시간 시각화</h3>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed mb-4">
              인터랙티브 차트와 지도로 직관적인 데이터 표현
            </p>
            <div class="flex items-center justify-center text-xs text-gray-500">
              <span class="w-2 h-2 bg-emerald-400 rounded-full mr-2"></span>
              차트, 지도 시각화
            </div>
          </div>
        </div>

      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <!-- 복합 추론 진행 상태 (query3) -->
        <div v-if="complexReasoningProgress.isActive" class="max-w-2xl mx-auto">
          <div class="bg-white rounded-2xl shadow-xl border border-gray-200/60 p-8 mb-6">
            <div class="flex items-center justify-center mb-6">
              <div class="relative">
                <div class="w-16 h-16 border-4 border-indigo-200 rounded-full animate-spin"></div>
                <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-indigo-600 rounded-full animate-spin"></div>
              </div>
            </div>
            
            <h3 class="text-xl font-bold text-gray-800 mb-2">
              {{ complexReasoningProgress.stepTitle }}
            </h3>
            <p class="text-gray-600 mb-4">
              {{ complexReasoningProgress.stepDescription }}
            </p>
            
            <!-- 진행률 바 -->
            <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
              <div 
                class="bg-gradient-to-r from-purple-500 to-indigo-600 h-2 rounded-full transition-all duration-500 ease-out"
                :style="{ width: `${(complexReasoningProgress.currentStep / complexReasoningProgress.totalSteps) * 100}%` }"
              ></div>
            </div>
            
            <p class="text-gray-500 text-sm">
              단계 {{ complexReasoningProgress.currentStep }} / {{ complexReasoningProgress.totalSteps }}
            </p>
          </div>
        </div>
        
        <!-- 일반 로딩 상태 -->
        <div v-else>
          <div class="relative inline-flex items-center justify-center mb-6">
            <div class="w-24 h-24 rounded-full flex items-center justify-center">
              <div class="relative">
                <div class="w-12 h-12 border-4 border-indigo-200 rounded-full animate-spin"></div>
                <div class="absolute inset-0 w-12 h-12 border-4 border-transparent border-t-indigo-600 rounded-full animate-spin"></div>
              </div>
            </div>
            <!-- <div class="absolute -inset-4 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-pink-500/20 rounded-full blur-xl animate-pulse"></div> -->
          </div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">
            {{ isAdvancedQuery ? '복합 추론을 진행하고 있습니다...' : '데이터를 분석하고 있습니다...' }}
          </h3>
          <p class="text-gray-600 max-w-md mx-auto">잠시만 기다려 주세요</p>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="result && !loading" class="space-y-8">

        <!-- 1. Analysis Section -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <h3 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="w-8 h-8 bg-amber-100 text-amber-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">1</span>
              분석 결과
            </h3>
          </div>
          <div class="px-6 lg:px-8 py-8">
            <div v-if="result.analysis">
              <!-- 키워드 박스탭 -->
              <div v-if="analysisKeywords.length > 0" class="mb-8">
                <h4 class="text-lg font-semibold text-gray-800 mb-4 flex">
                  <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-lg text-xs font-bold flex items-center justify-center mr-2">📊</span>
                  핵심 인사이트
                </h4>
                <div class="flex flex-wrap gap-3">
                  <span 
                    v-for="keyword in analysisKeywords" 
                    :key="keyword.text"
                    :class="[
                      'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 hover:scale-105',
                      keyword.type === 'highlight' ? 'bg-yellow-100 text-yellow-800 border border-yellow-200' :
                      keyword.type === 'number' ? 'bg-green-100 text-green-800 border border-green-200' :
                      keyword.type === 'location' ? 'bg-purple-100 text-purple-800 border border-purple-200' :
                      'bg-blue-100 text-blue-800 border border-blue-200'
                    ]"
                  >
                    {{ keyword.text }}
                  </span>
                </div>
              </div>

              <!-- 상세 분석 내용 -->
              <div class="prose prose-gray max-w-none">
                <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <span class="w-6 h-6 bg-gray-100 text-gray-600 rounded-lg text-xs font-bold flex items-center justify-center mr-2">📝</span>
                  상세 분석
                </h4>
                <div v-html="formattedAnalysis" class="text-gray-700 leading-relaxed text-base bg-gray-50 rounded-xl p-6 border border-gray-200"></div>
              </div>

              <!-- 추가 분석 제안 (query2인 경우에만 표시) -->
              <div v-if="result.queryType === 2" class="mt-8 pt-6 border-t border-gray-200">
                <h4 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <span class="w-6 h-6 bg-purple-100 text-purple-600 rounded-lg text-xs font-bold flex items-center justify-center mr-2">💡</span>
                  추가 분석 제안
                </h4>
                <div class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-200">
                  <p class="text-gray-700 mb-4 font-medium">
                    소득 분포 분석을 바탕으로 더 깊이 있는 인사이트를 발견해보세요.
                  </p>
                  <button
                    @click="onClickExecuteAdvancedQuery"
                    :disabled="loading"
                    class="group flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div v-if="loading" class="animate-spin w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full"></div>
                    <svg v-else class="w-4 h-4 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                    </svg>
                    <span class="text-sm font-medium">예시: 지역별 전기차 충전소 개수는 소득 수준과 상관성이 있을까?</span>
                  </button>
                  <!-- <p class="text-sm text-gray-600 mt-3">
                    고급 분석을 통해 소득과 전기차 충전소 간의 상관관계를 분석합니다.
                  </p> -->
                </div>
              </div>
            </div>
            <div v-else class="text-gray-500 text-center py-8">
              분석 결과가 없습니다.
            </div>
          </div>
        </div>

        <!-- 2. Visualization Section -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-bold text-gray-800 flex items-center">
                <span class="w-8 h-8 bg-purple-100 text-purple-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">2</span>
                <span v-if="shouldShowMap">충전소 위치 지도</span>
                <span v-else-if="result.queryType === 3">복지 취약성 분석</span>  
                <span v-else-if="result.queryType === 4">소득과 충전소 상관관계 분석</span>
                <span v-else>데이터 시각화</span>
              </h3>
              
              <!-- 복지 분석 차트 타입 선택 버튼 -->
              <div v-if="result.queryType === 3" class="flex gap-2">
                <button
                  @click="welfareChartType = 'line'"
                  :class="[
                    'px-3 py-1 text-xs rounded-full transition-colors',
                    welfareChartType === 'line' 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  ]"
                >
                  지역별 현황
                </button>
                <button
                  @click="welfareChartType = 'bar'"
                  :class="[
                    'px-3 py-1 text-xs rounded-full transition-colors',
                    welfareChartType === 'bar' 
                      ? 'bg-purple-500 text-white' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  ]"
                >
                  종합점수
                </button>
              </div>
            </div>
          </div>
          
          <div class="px-6 lg:px-8 py-8">
            <!-- Map for Query 1 - Charging Stations -->
            <div v-if="shouldShowMap" class="h-96 relative rounded-lg overflow-hidden border border-gray-200">
              <div ref="mapContainer" class="w-full h-full"></div>
            </div>
            
            <!-- Welfare Analysis Charts for Query 3 -->
            <div v-else-if="result.queryType === 3" class="h-[500px] relative">
              <!-- 데이터 없음 안내 -->
              <div v-if="!hasWelfareChartData" class="flex items-center justify-center h-full">
                <div class="text-gray-400 text-base">시각화할 데이터가 없습니다.</div>
              </div>
              <!-- Line Chart for Regional Status -->
              <div v-else class="h-full w-full flex flex-col">
                <div :class="{ 'hidden': welfareChartType !== 'line' }" class="h-full w-full flex-1">
                  <canvas ref="welfareLineChart" style="width:100%;height:100%;display:block;"></canvas>
                </div>
                <!-- Bar Chart for Comprehensive Score -->
                <div :class="{ 'hidden': welfareChartType !== 'bar' }" class="h-full w-full flex-1">
                  <canvas ref="welfareBarChart" style="width:100%;height:100%;display:block;"></canvas>
                </div>
              </div>
            </div>
            
            <!-- Scatter Chart for Query 4 -->
            <div v-else-if="shouldShowScatterChart" class="h-[500px] relative">
              <!-- 로딩 중일 때 스켈레톤 표시 -->
              <div v-if="loading" class="bg-gray-100 rounded-xl p-4 animate-pulse">
                <div class="h-6 bg-gray-200 rounded mb-4"></div>
                <div class="h-80 bg-gray-200 rounded"></div>
              </div>
              
              <!-- 실제 산점도 차트 -->
              <div v-else class="relative w-full h-[500px]">
                <canvas ref="chartCanvas" style="width:100%;height:100%"></canvas>
              </div>
            </div>
            
            <!-- Bar Chart for Query 2 -->
            <div v-else-if="shouldShowBarChart" class="h-[400px] relative">
              <!-- Query 2: 소득 분포 - 로딩 상태 표시 추가 -->
              <div v-if="result.queryType === 2">
                <!-- 로딩 중일 때 스켈레톤 표시 -->
                <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
                  <div class="bg-gray-100 rounded-xl p-4 animate-pulse">
                    <div class="h-6 bg-gray-200 rounded mb-4"></div>
                    <div class="h-80 bg-gray-200 rounded"></div>
                  </div>
                  <div class="bg-gray-100 rounded-xl p-4 animate-pulse">
                    <div class="h-6 bg-gray-200 rounded mb-4"></div>
                    <div class="h-80 bg-gray-200 rounded"></div>
                  </div>
                </div>
                
                <!-- 실제 차트 -->
                <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
                  <div class="bg-gray-50 rounded-xl p-4">
                    <h4 class="text-lg font-semibold text-gray-800 mb-4 text-center">상위 10개 지역</h4>
                    <div class="h-80">
                      <canvas ref="topChartCanvas" style="width:100%;height:100%"></canvas>
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded-xl p-4">
                    <h4 class="text-lg font-semibold text-gray-800 mb-4 text-center">하위 10개 지역</h4>
                    <div class="h-80">
                      <canvas ref="bottomChartCanvas" style="width:100%;height:100%"></canvas>
                    </div>
                  </div>
                </div>
              </div>
              
            </div>
            <!-- Pie Chart for Query 3 (legacy) -->
            <div v-else-if="shouldShowPieChart" class="h-96 relative">
              <canvas ref="pieChartCanvas"></canvas>
            </div>

            <!-- No Chart Available -->
            <div v-else class="h-96 flex items-center justify-center text-gray-500">
              <div class="text-center">
                <div class="text-4xl mb-4">📊</div>
                <p class="text-lg">시각화할 수 있는 데이터가 없습니다</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 2.5. Reasoning Steps Section (Advanced queries only) -->
        <div v-if="result.reasoningSteps?.length" class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <h3 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="w-8 h-8 bg-rose-100 text-rose-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">🧠</span>
              추론 과정
            </h3>
          </div>
          <div class="px-6 lg:px-8 py-8">
            <div class="space-y-6">
              <div v-for="step in result.reasoningSteps" :key="step.step" 
                   class="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl border border-gray-200">
                <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-lg flex items-center justify-center text-sm font-bold">
                  {{ step.step }}
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-800 mb-2">{{ step.title }}</h4>
                  <p class="text-gray-600 text-sm mb-2">{{ step.description }}</p>
                  <div class="text-xs text-gray-500 bg-white px-3 py-2 rounded-lg border">
                    <code>{{ step.detail }}</code>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 3. SPARQL Query Section -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <div class="flex items-center justify-between">
              <h3 class="text-xl font-bold text-gray-800 flex items-center">
                <span class="w-8 h-8 bg-indigo-100 text-indigo-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">3</span>
                실행된 SPARQL 쿼리
              </h3>
              <button
                @click="showQuery = !showQuery"
                class="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg transition-colors text-sm font-medium"
              >
                {{ showQuery ? '접기' : '펼치기' }}
                <span class="transform transition-transform" :class="{ 'rotate-180': showQuery }">
                  ▼
                </span>
              </button>
            </div>
          </div>
          
          <div v-if="showQuery" class="px-6 lg:px-8 pb-6">
            <div class="bg-gray-900 rounded-xl p-6 overflow-x-auto">
              <pre class="text-green-400 text-sm whitespace-pre-wrap font-mono leading-relaxed">{{ result.sparqlQuery }}</pre>
            </div>
          </div>
        </div>

        <!-- 4. Results Table Section -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <h3 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="w-8 h-8 bg-emerald-100 text-emerald-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">4</span>
              쿼리 결과 예시
            </h3>
          </div>
          <div v-if="tableColumns.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-200">
                  <th v-for="column in tableColumns" :key="column" 
                      class="px-6 py-4 text-left font-semibold text-gray-700 text-sm">
                    {{ column }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in displayResults" :key="idx" 
                    class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td v-for="column in tableColumns" :key="column" class="px-6 py-4 text-gray-600 text-sm">
                    {{ formatCellValue(row[column]) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="px-6 py-8 text-center text-gray-500">
            표시할 데이터가 없습니다.
          </div>
          <div v-if="result.results && result.results.length > 10" class="px-6 lg:px-8 py-4 bg-gray-50 border-t border-gray-100">
            <p class="text-sm text-gray-500">
              총 <span class="font-semibold text-gray-700">{{ result.results.length }}개</span> 결과 중 상위 5개만 표시
            </p>
          </div>
        </div>

        <!-- 5. Data Source -->
        <div class="bg-white rounded-2xl shadow-lg border border-gray-200/60 overflow-hidden">
          <div class="px-6 lg:px-8 py-6 border-b border-gray-100">
            <h3 class="text-xl font-bold text-gray-800 flex items-center">
              <span class="w-8 h-8 bg-blue-100 text-blue-600 rounded-lg text-sm font-bold flex items-center justify-center mr-3">5</span>
              데이터 출처
            </h3>
          </div>

          <div class="px-6 lg:px-8 py-6">
            <div v-if="result.queryType === 1" class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-indigo-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                    <div class="flex">
                        <h4 class="font-semibold text-gray-800 mb-1"><a href="https://www.data.go.kr/data/15013115/standard.do" 
                     target="_blank">전국전기차충전소표준데이터</a></h4>
                        <a href="https://www.data.go.kr/data/15013115/standard.do" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            class="inline-flex items-center gap-3 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
                            <span class="ml-2">🔗</span>
                        </a>
                    </div>
                <!-- <p class="text-sm text-gray-600 mb-2">전국의 전기차 충전소 위치 및 운영 정보를 제공하는 공공데이터</p> -->
                </div>
              </div>
            </div>
            
            <div v-else-if="result.queryType === 2" class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div>
                <div class="flex">
                  <h4 class="font-semibold text-gray-800 mb-1">지역별 소득 데이터</h4>
                      <a href="https://www.data.go.kr/data/15082063/fileData.do" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          class="inline-flex items-center gap-3 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
                          <span class="ml-2">🔗</span>
                        </a>
                  <!-- <p class="text-sm text-gray-600 mb-2">통계청 및 관련 기관에서 제공하는 지역별 평균소득 통계 정보</p> -->
                </div>
              </div>
            </div>

            <div v-else-if="result.queryType === 3" class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="flex">
                  <!-- <div class="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div> -->
                  <h4 class="font-semibold text-gray-800 mb-1">전국버스정류장위치데이터</h4>
                      <a href="https://www.data.go.kr/data/15067528/fileData.do" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          class="inline-flex items-center gap-3 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
                          <span class="ml-2">🔗</span>
                        </a>
                  <!-- <p class="text-sm text-gray-600 mb-2">통계청 및 관련 기관에서 제공하는 지역별 평균소득 통계 정보</p> -->
                </div>

                <div class="flex">
                  <!-- <div class="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div> -->
                  <h4 class="font-semibold text-gray-800 mb-1">전국복지수급데이터</h4>
                      <a href="https://www.data.go.kr/data/15067528/fileData.do" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          class="inline-flex items-center gap-3 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
                          <span class="ml-2">🔗</span>
                        </a>
                  <!-- <p class="text-sm text-gray-600 mb-2">통계청 및 관련 기관에서 제공하는 지역별 평균소득 통계 정보</p> -->
                </div>

                <div class="flex">
                  <!-- <div class="w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></div> -->
                  <h4 class="font-semibold text-gray-800 mb-1">행정구역표준데이터(인구수, 면적)</h4>
                      <a href="https://www.data.go.kr/data/15067528/fileData.do" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          class="inline-flex items-center gap-3 text-sm text-indigo-600 hover:text-indigo-800 transition-colors">
                          <span class="ml-2">🔗</span>
                        </a>
                  <!-- <p class="text-sm text-gray-600 mb-2">통계청 및 관련 기관에서 제공하는 지역별 평균소득 통계 정보</p> -->
                </div>
              </div>
            </div>
          
            <div v-else-if="result.queryType === 4" class="space-y-4">
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-1">복지 수급 및 교통 데이터</h4>
                  <p class="text-sm text-gray-600 mb-2">보건복지부, 국토교통부 등에서 제공하는 복지 수급 현황 및 대중교통 인프라 정보</p>
                  <div class="text-sm text-gray-500">
                    <span>🏛️</span>
                    <span class="ml-1">보건복지부, 국토교통부, 지자체 공공데이터 활용</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 공통 메시지 -->
            <!-- <div class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div class="flex items-start space-x-2">
                <span class="text-gray-500 text-sm mt-0.5">ℹ️</span>
                <div class="text-sm text-gray-600">
                  <p class="font-medium mb-1">데이터 품질 및 최신성</p>
                  <p>모든 데이터는 공공기관에서 공식적으로 제공하는 정보를 기반으로 하며, 정기적으로 업데이트됩니다. 단, 데이터 수집 시점에 따라 최신 정보와 차이가 있을 수 있습니다.</p>
                </div>
              </div>
            </div> -->
          </div>
        </div>

        <!-- Error State -->
        <div v-if="result && !result.success" class="bg-red-50 border border-red-200 rounded-2xl p-8 shadow-lg">
          <h3 class="font-semibold text-red-800 mb-3 text-lg flex items-center">
            <span class="mr-2">⚠️</span>
            오류 발생
          </h3>
          <p class="text-red-600">{{ result.error }}</p>
        </div>
      </div>

    </div>

    <!-- Footer -->
    <div class="bg-white/90 backdrop-blur-xl shadow-sm border-t border-gray-100/80 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h4 class="text-sm font-normal text-gray-500 mb-2">지식그래프 엔진</h4>
            <p class="text-xs text-gray-400">Shannon Knowledge Graph</p>
          </div>
          <div>
            <h4 class="text-sm font-normal text-gray-500 mb-2">문의</h4>
            <p class="text-xs text-gray-400">hike.cau@gmail.com</p>
          </div>
          <div>
            <h4 class="text-sm font-normal text-gray-500 mb-2">업데이트</h4>
            <p class="text-xs text-gray-400">2025년 9월</p>
          </div>
        </div>
        <div class="mt-10">
            <p class="mt-10 text-xs text-gray-400 text-center">© 2025 Shannon Insight - Advanced Knowledge Graph Analytics</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onUnmounted, onMounted } from 'vue'
// 복지 차트 데이터 존재 여부
const hasWelfareChartData = computed(() => {
  if (result.value?.queryType !== 3) return false
  const regions = result.value?.data?.welfare_analysis?.regions
  if (regions && Array.isArray(regions) && regions.length > 0) return true
  if (result.value?.results && Array.isArray(result.value.results) && result.value.results.length > 0) return true
  return false
})

const userQuery = ref('')
const result = ref(null)
const loading = ref(false)
const showQuery = ref(false)
const chartCanvas = ref(null)
const pieChartCanvas = ref(null)
const mapContainer = ref(null)
const welfareLineChart = ref(null)
const welfareBarChart = ref(null)
const topChartCanvas = ref(null)
const bottomChartCanvas = ref(null)
const welfareChartType = ref('line')
const isAdvancedQuery = ref(false)
const currentTipIndex = ref(0)

// 복합 추론 진행 상태 관리
const complexReasoningProgress = ref({
  isActive: false,
  currentStep: 0,
  totalSteps: 3,
  stepTitle: '',
  stepDescription: ''
})

let currentChart = null
let currentPieChart = null
let currentWelfareLineChart = null
let currentWelfareBarChart = null
let currentTopChart = null
let currentBottomChart = null
let currentMap = null
let currentTileLayer = null
const currentMapStyle = ref('openstreetmap')

// const API_BASE_URL = 'http://localhost:8001/api'

const config = useRuntimeConfig()
const API_BASE_URL = config.public.apiUrl

const mapStyleOptions = {
  openstreetmap: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '© OpenStreetMap contributors',
    name: 'OSM'
  },
  cartodb: {
    url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    attribution: '© OpenStreetMap contributors © CARTO',
    name: 'Light'
  }
}

const sampleQueries = [
  { title: '전기차 충전소', query: '서울특별시 동작구의 전기차 충전소 위치를 확인해줘', difficulty: 'basic' },
  { title: '소득 분포', query: '지역별 소득 분포 현황을 분석해줘', difficulty: 'basic' },
  { title: '복지수급 + 버스정류장', query: '면적 대비 버스정류장 수와 복지수급자 수의 비율이 낮은 지역은 어디야?', difficulty: 'advanced' }
]

const analysisTips = [
  {
    title: '구체적인 질문하기',
    description: '"서울시 강남구 전기차 충전소 현황"처럼 구체적으로 질문하면 더 정확한 분석을 받을 수 있습니다.',
    icon: 'search',
    example: '예: "서울시 강남구 전기차 충전소 현황"'
  },
  {
    title: '연관성 찾기',
    description: '"소득과 교통시설 관계"처럼 두 데이터 간의 관계를 질문하면 흥미로운 인사이트를 발견할 수 있습니다.',
    icon: 'chart',
    example: '예: "소득과 교통시설 관계"'
  },
  {
    title: '트렌드 분석',
    description: '"최근 3년간 변화 추이"나 "지역별 비교"와 같은 시간/공간 관점의 질문도 유용합니다.',
    icon: 'trend',
    example: '예: "최근 3년간 변화 추이"'
  }
]

// 자동 슬라이더 로직
let tipSliderInterval = null

const startTipSlider = () => {
  tipSliderInterval = setInterval(() => {
    currentTipIndex.value = (currentTipIndex.value + 1) % analysisTips.length
  }, 4000)
}

const stopTipSlider = () => {
  if (tipSliderInterval) {
    clearInterval(tipSliderInterval)
    tipSliderInterval = null
  }
}

// onMounted 추가 (기존 함수들 뒤에)
if (process.client) {
  startTipSlider()
}

// 나머지 computed properties와 functions는 기존 코드와 동일하게 유지
const tableColumns = computed(() => {
  if (!result.value?.results?.length) return []
  
  if (result.value.queryType === 3) {
    if (result.value.data?.welfare_analysis?.regions?.length) {
      const sampleRow = result.value.data.welfare_analysis.regions[0]
      return Object.keys(sampleRow)
    }
    
    if (result.value.results?.length) {
      return Object.keys(result.value.results[0])
    }
    
    return ['지역명', '면적', '복지수급자수', '버스정류장수', '복지밀도', '버스밀도', '종합점수']
  }
  
  return Object.keys(result.value.results[0])
})

const displayResults = computed(() => {
  if (!result.value?.results) return []
  
  if (result.value.queryType === 3) {
    if (result.value.data?.welfare_analysis?.regions?.length) {
      return result.value.data.welfare_analysis.regions.slice(0, 5)
    }
  }
  
  return result.value.results.slice(0, 5)
})

const shouldShowMap = computed(() => {
  if (result.value?.queryType !== 1 || !result.value.results?.length) {
    return false
  }
  
  const firstResult = result.value.results[0]
  const hasCoords = firstResult?.위도 && firstResult?.경도
  return hasCoords
})

const shouldShowBarChart = computed(() => {
  // queryType만 확인하고, 로딩 중이거나 결과가 있으면 표시
  return result.value?.queryType && [2].includes(result.value.queryType) && 
         (loading.value || (result.value.results?.length > 0))
})

const shouldShowAdvancedChart = computed(() => {
  return result.value?.queryType === 4 && result.value.data?.districts?.length > 0
})

const shouldShowScatterChart = computed(() => {
  return result.value?.queryType === 4 && 
         (loading.value || (result.value.data?.districts?.length > 0))
})

const shouldShowPieChart = computed(() => {
  return false
})

const analysisKeywords = computed(() => {
  return result.value?.keywords || []
})

const formattedAnalysis = computed(() => {
  if (!result.value?.analysis) return ''
  return result.value.analysis
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
})

const formatCellValue = (value) => {
  if (value === null || value === undefined || value === '') return '-'
  
  if (typeof value === 'number' || (typeof value === 'string' && !isNaN(parseFloat(value)))) {
    const num = parseFloat(value)
    
    if (isNaN(num)) return String(value)
    
    if (num % 1 !== 0) {
      return num.toFixed(2)
    }
    
    return num.toLocaleString()
  }
  
  return String(value)
}

const executeQuery = async () => {
  if (!userQuery.value.trim()) return
  
  isAdvancedQuery.value = sampleQueries.some(sample => 
    sample.difficulty === 'advanced' && userQuery.value.includes(sample.title.split(' ')[0])
  ) || userQuery.value.includes('비율') || userQuery.value.includes('복합') || userQuery.value.includes('추론')
  
  loading.value = true
  result.value = null
  welfareChartType.value = 'line'
  destroyCharts()
  
  complexReasoningProgress.value = {
    isActive: false,
    currentStep: 0,
    totalSteps: 3,
    stepTitle: '',
    stepDescription: ''
  }
  
  try {
    const queryType = determineQueryType(userQuery.value)
    
    if (queryType === 3) {
      complexReasoningProgress.value.isActive = true
      await simulateComplexReasoningSteps()
    }
    
    const response = await fetch(`${API_BASE_URL}/query/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        query: userQuery.value,
        queryType: queryType
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    result.value = {
      success: data.success,
      queryType: data.queryType,
      sparqlQuery: data.sparqlQuery,
      data: data.data,
      results: data.results,
      analysis: data.analysis,
      keywords: data.keywords || [],
      reasoningSteps: isAdvancedQuery.value ? generateReasoningSteps(data.queryType) : null,
      error: data.success ? null : data.message
    }

    if (data.success && data.results?.length) {
      // Query2의 경우 특별한 처리
      if (data.queryType === 2) {
        console.log('Query2 detected, preparing for chart rendering...')
        
        // DOM 업데이트 대기
        await nextTick()
        
        // 추가 안정화 대기
        await new Promise(resolve => setTimeout(resolve, 400))
        
        console.log('Starting chart drawing for Query2...')
      } else {
        await nextTick()
      }
      
      await drawChart()
    }
    
  } catch (err) {
    console.error('Query execution error:', err)
    result.value = { 
      success: false, 
      error: `분석 중 오류가 발생했습니다: ${err.message}`
    }
  } finally {
    loading.value = false
    complexReasoningProgress.value.isActive = false
  }
}


const debugCanvasState = () => {
  console.log('=== Canvas Debug Info ===')
  console.log('shouldShowBarChart:', shouldShowBarChart.value)
  console.log('topChartCanvas exists:', !!topChartCanvas.value)
  console.log('bottomChartCanvas exists:', !!bottomChartCanvas.value)
  
  if (topChartCanvas.value) {
    const topRect = topChartCanvas.value.getBoundingClientRect()
    console.log('topCanvas size:', topRect.width, 'x', topRect.height)
    console.log('topCanvas connected:', topChartCanvas.value.isConnected)
  }
  
  if (bottomChartCanvas.value) {
    const bottomRect = bottomChartCanvas.value.getBoundingClientRect()
    console.log('bottomCanvas size:', bottomRect.width, 'x', bottomRect.height)
    console.log('bottomCanvas connected:', bottomChartCanvas.value.isConnected)
  }
  
  console.log('currentTopChart:', !!currentTopChart)
  console.log('currentBottomChart:', !!currentBottomChart)
  console.log('========================')
}

const executeAdvancedQuery = async () => {
  loading.value = true
  destroyCharts()

  // 복지 분석 진행 상태 설정 (query3)
  complexReasoningProgress.value = {
    isActive: true,
    currentStep: 0,
    totalSteps: 3,
    stepTitle: '',
    stepDescription: ''
  }

  try {
    await simulateComplexReasoningSteps()

    const response = await fetch(`${API_BASE_URL}/query/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: '복지 취약성 분석',
        queryType: 3
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    result.value = {
      success: data.success,
      queryType: data.queryType,
      sparqlQuery: data.sparqlQuery,
      data: data.data,
      results: data.results,
      analysis: data.analysis,
      keywords: data.keywords || [],
      reasoningSteps: generateReasoningSteps(3),
      error: data.success ? null : data.message
    }

    if (data.success && data.results?.length) {
      await nextTick()
      await drawChart()
    }

  } catch (err) {
    console.error('복지 분석 실행 오류:', err)
    result.value = {
      success: false,
      error: `복지 분석 중 오류가 발생했습니다: ${err.message}`
    }
  } finally {
    loading.value = false
    complexReasoningProgress.value.isActive = false
  }
}

// 나머지 함수들도 기존과 동일하게 유지하되, 여기서는 생략
const determineQueryType = (query) => {
  const q = query.toLowerCase()
  if (q.includes('전기차') || q.includes('충전소')) return 1
  if (q.includes('소득') || q.includes('경제')) return 2
  if (q.includes('복지') || q.includes('수급')) return 3
  if (q.includes('버스') || q.includes('정류장')) return 4
  return 1
}

const generateReasoningSteps = (queryType) => {
  if (queryType === 3) {
    return [
      {
        step: 1,
        title: "행정구역 기본 정보 수집",
        description: "각 지역의 행정구역명, 면적, 인구수 등 기본 정보를 수집합니다.",
        detail: "schema:AdministrativeArea를 통해 지역별 기본 정보를 추출"
      },
      {
        step: 2,
        title: "복지수급자 데이터 집계",
        description: "지역별 복지수급자 수를 합산하여 총 수급자 규모를 파악합니다.",
        detail: "schema:GovernmentService의 numberOfEmployees를 지역별로 GROUP BY 집계"
      },
      {
        step: 3,
        title: "교통 인프라 현황 분석",
        description: "각 지역의 버스정류장 개수를 계산하여 교통 접근성을 측정합니다.",
        detail: "schema:BusStop을 지역별로 COUNT하여 교통 인프라 밀도 계산"
      },
      {
        step: 4,
        title: "면적 대비 밀도 지표 계산",
        description: "복지수급자 밀도와 버스정류장 밀도를 면적 대비로 정규화합니다.",
        detail: "복지밀도 = 복지수급자수 / 면적, 버스밀도 = 버스정류장수 / 면적"
      },
      {
        step: 5,
        title: "종합 취약성 점수 산출",
        description: "복지 수요는 높지만 교통 접근성이 낮은 지역을 식별하는 종합 점수를 계산합니다.",
        detail: "종합점수 = (복지밀도 × 10) - (버스밀도 × 5), 높을수록 취약"
      }
    ]
  }
  return []
}

const generateAdvancedReasoningSteps = () => {
  return [
    {
      step: 1,
      title: "소득 데이터 수집 및 검증",
      description: "지역별 평균소득 데이터를 수집하고 데이터 품질을 검증합니다.",
      detail: "schema:AdministrativeArea의 amount 속성을 통해 지역별 소득 정보 추출"
    },
    {
      step: 2,
      title: "전기차 충전소 위치 데이터 분석",
      description: "각 지역에 설치된 전기차 충전소의 개수를 계산합니다.",
      detail: "schema:ElectricVehicleChargingStation을 지역별로 COUNT하여 충전소 밀도 계산"
    },
    {
      step: 3,
      title: "상관관계 분석 수행",
      description: "소득 수준과 충전소 개수 간의 상관관계를 통계적으로 분석합니다.",
      detail: "소득과 충전소 수의 피어슨 상관계수 계산 및 유의성 검정"
    },
    {
      step: 4,
      title: "지역별 패턴 식별",
      description: "고소득 지역과 저소득 지역의 충전소 분포 패턴을 비교 분석합니다.",
      detail: "소득 구간별 충전소 밀도 차이 분석 및 통계적 유의성 검정"
    },
    {
      step: 5,
      title: "정책 인사이트 도출",
      description: "분석 결과를 바탕으로 전기차 보급 정책에 대한 인사이트를 도출합니다.",
      detail: "지역별 맞춤형 충전 인프라 확충 방안 및 정책 제언 도출"
    }
  ]
}

// 복합 추론 단계별 진행 시뮬레이션
const simulateComplexReasoningSteps = async () => {
  const steps = [
    {
      step: 1,
      title: "데이터 확인 중",
      description: "관련 데이터를 확인하고 검증합니다.",
      duration: 5000
    },
    {
      step: 2,
      title: "분석 진행 중",
      description: "복합 추론 분석을 수행하고 있습니다.",
      duration: 10000
    },
    {
      step: 3,
      title: "분석 결과 정리 중",
      description: "분석 결과를 정리하고 시각화를 준비합니다.",
      duration: 10000
    }
  ]

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i]
    
    // 현재 단계 업데이트
    complexReasoningProgress.value.currentStep = step.step
    complexReasoningProgress.value.stepTitle = step.title
    complexReasoningProgress.value.stepDescription = step.description
    
    // 각 단계마다 지정된 시간만큼 대기
    await new Promise(resolve => setTimeout(resolve, step.duration))
  }
}

// 고급 분석 단계별 진행 시뮬레이션 (query4용)
const simulateAdvancedReasoningSteps = async () => {
  const steps = [
    {
      step: 1,
      title: "소득 데이터 수집 중",
      description: "지역별 소득 데이터를 수집하고 검증합니다.",
      duration: 3000
    },
    {
      step: 2,
      title: "충전소 데이터 분석 중",
      description: "전기차 충전소 위치 데이터를 분석합니다.",
      duration: 4000
    },
    {
      step: 3,
      title: "상관관계 계산 중",
      description: "소득과 충전소 간의 상관관계를 계산합니다.",
      duration: 5000
    },
    {
      step: 4,
      title: "결과 정리 중",
      description: "분석 결과를 정리하고 인사이트를 도출합니다.",
      duration: 3000
    }
  ]

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i]
    
    // 현재 단계 업데이트
    complexReasoningProgress.value.currentStep = step.step
    complexReasoningProgress.value.stepTitle = step.title
    complexReasoningProgress.value.stepDescription = step.description
    
    // 각 단계마다 지정된 시간만큼 대기
    await new Promise(resolve => setTimeout(resolve, step.duration))
  }
}

const loadSampleQuery = (index) => {
  if (index >= 0 && index < sampleQueries.length) {
    userQuery.value = sampleQueries[index].query
  }
}

const refreshPage = () => {
  window.location.reload()
}

const clearResults = () => {
  result.value = null
  userQuery.value = ''
  showQuery.value = false
  destroyCharts()
}

const destroyCharts = () => {
  if (currentChart) {
    currentChart.destroy()
    currentChart = null
  }
  if (currentPieChart) {
    currentPieChart.destroy()
    currentPieChart = null
  }
  if (currentWelfareLineChart) {
    currentWelfareLineChart.destroy()
    currentWelfareLineChart = null
  }
  if (currentWelfareBarChart) {
    currentWelfareBarChart.destroy()
    currentWelfareBarChart = null
  }
  if (currentTopChart) {
    currentTopChart.destroy()
    currentTopChart = null
  }
  if (currentBottomChart) {
    currentBottomChart.destroy()
    currentBottomChart = null
  }
  if (currentMap) {
    currentMap.remove()
    currentMap = null
  }
  currentTileLayer = null
}

// 4. drawChart 함수에서 query2 특별 처리
const drawChart = async () => {
  if (!result.value?.results?.length) {
    console.log('No results available for chart drawing')
    return
  }

  try {
    const queryType = result.value.queryType
    console.log(`Drawing chart for queryType: ${queryType}`)

    if (queryType === 1 && shouldShowMap.value) {
      await drawMap()
    } else if (queryType === 2) {
      // Query2의 경우 더 신중한 처리
      console.log('Preparing for Query2 income charts...')
      
      const { Chart, registerables } = await import('chart.js')
      Chart.register(...registerables)
      
      // DOM 완전 준비 대기 (더 길게)
      await nextTick()
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // shouldShowBarChart가 true인지 재확인
      if (!shouldShowBarChart.value) {
        console.log('Bar chart should not be shown, skipping...')
        return
      }
      
      await drawIncomeCharts(Chart)
      
    } else if (queryType === 3) {
      const { Chart, registerables } = await import('chart.js')
      Chart.register(...registerables)
      
      // DOM 업데이트 대기
      await nextTick()
      await new Promise(resolve => setTimeout(resolve, 300))
      
      await drawWelfareCharts(Chart)
    } else if (queryType === 4) {
      const { Chart, registerables } = await import('chart.js')
      Chart.register(...registerables)
      await drawScatterChart(Chart)
    }
  } catch (error) {
    console.error('Chart drawing error:', error)
    
    // 한 번만 재시도
    if (!error.retried && result.value?.queryType === 2) {
      error.retried = true
      console.log('Retrying chart drawing in 1 second...')
      setTimeout(() => drawChart(), 1000)
    }
  }
}

// 복지 분석용 차트 그리기 함수 (진단 로그 추가)
const drawWelfareCharts = async (Chart, retryCount = 0) => {
  if (result.value?.queryType !== 3) {
    console.log(`복지 차트는 query3에서만 그립니다. 현재 queryType: ${result.value?.queryType}`)
    return
  }

  // 데이터 존재 여부 진단
  const regions = result.value?.data?.welfare_analysis?.regions
  const fallbackResults = result.value?.results
  console.log('[drawWelfareCharts] 데이터 진단:', {
    regionsType: typeof regions,
    regionsLen: Array.isArray(regions) ? regions.length : 'N/A',
    fallbackResultsLen: Array.isArray(fallbackResults) ? fallbackResults.length : 'N/A',
    welfareLineChartRef: !!welfareLineChart.value,
    welfareBarChartRef: !!welfareBarChart.value,
    welfareChartType: welfareChartType.value
  })

  if (!hasWelfareChartData.value) {
    console.warn('[drawWelfareCharts] 시각화할 데이터가 없습니다.')
    return
  }

  try {
    // DOM이 완전히 준비될 때까지 대기
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))
    // welfareChartType에 따라 해당 차트만 그리기
    if (welfareChartType.value === 'line') {
      await drawWelfareLineChart(Chart)
    } else if (welfareChartType.value === 'bar') {
      await drawWelfareBarChart(Chart)
    } else {
      // 혹시 모를 확장 대비
      await drawWelfareLineChart(Chart)
      await new Promise(resolve => setTimeout(resolve, 100))
      await drawWelfareBarChart(Chart)
    }
  } catch (error) {
    console.error('복지 차트 그리기 오류:', error)
    // 재시도 로직 (최대 2번)
    if (retryCount < 2) {
      console.log(`복지 차트 재시도 중... (${retryCount + 1}/2)`)
      await new Promise(resolve => setTimeout(resolve, 500))
      await drawWelfareCharts(Chart, retryCount + 1)
    }
  }
}

// welfareChartType이 바뀔 때마다 차트 다시 그림
watch(welfareChartType, async (newType, oldType) => {
  if (result.value?.queryType === 3 && hasWelfareChartData.value) {
    const { Chart, registerables } = await import('chart.js')
    Chart.register(...registerables)
    await nextTick()
    await drawWelfareCharts(Chart)
  }
})

// 복지 지역별 현황 라인 차트
const drawWelfareLineChart = async (Chart) => {
  // query3에서만 실행되도록 제한
  if (result.value?.queryType !== 3) {
    console.log('welfareLineChart는 query3에서만 그립니다.')
    return
  }

  // Canvas ref가 존재하는지 먼저 확인
  if (!welfareLineChart.value) {
    console.warn('welfareLineChart ref가 존재하지 않습니다. DOM에 렌더링되지 않았을 수 있습니다.')
    return
  }

  // Canvas 준비 상태 확인
  const canvasReady = await waitForCanvasReady(welfareLineChart, 'WelfareLineChart')
  if (!canvasReady) {
    console.warn('welfareLineChart canvas가 준비되지 않았습니다')
    return
  }

  // 기존 차트 정리
  if (currentWelfareLineChart) {
    currentWelfareLineChart.destroy()
    currentWelfareLineChart = null
  }

  try {
    const ctx = welfareLineChart.value.getContext('2d')
    
    // 데이터 소스 결정 (백엔드 처리 데이터 우선)
    let regions = []
    if (result.value.data?.welfare_analysis?.regions?.length) {
      regions = result.value.data.welfare_analysis.regions.slice(0, 8)
      console.log('백엔드 처리 데이터 사용:', regions.length, '개 지역')
    } else if (result.value.results?.length) {
      regions = result.value.results.slice(0, 8)
      console.log('원본 SPARQL 결과 사용:', regions.length, '개 지역')
    } else {
      console.warn('표시할 데이터가 없습니다')
      return
    }

    // 데이터 추출 및 안전한 변환
    const labels = regions.map(r => {
      const name = r.지역명 || r.region || '알 수 없음'
      return String(name).length > 10 ? String(name).substring(0, 10) + '...' : String(name)
    })
    
    const areaData = regions.map(r => {
      const area = parseFloat(r.면적 || r.area || 0)
      return isNaN(area) ? 0 : area
    })
    
    const welfareData = regions.map(r => {
      const welfare = parseInt(r.복지수급자수 || r.welfare_count || 0)
      return isNaN(welfare) ? 0 : welfare
    })
    
    const busData = regions.map(r => {
      const bus = parseInt(r.버스정류장수 || r.bus_count || 0)
      return isNaN(bus) ? 0 : bus
    })
    
    console.log('차트 데이터 확인:', {
      labels: labels.length,
      areas: areaData.filter(v => v > 0).length,
      welfare: welfareData.filter(v => v > 0).length,
      bus: busData.filter(v => v > 0).length
    })

    currentWelfareLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: '면적 (km²)',
            data: areaData,
            borderColor: '#10B981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            yAxisID: 'y'
          },
          {
            label: '복지수급자수 (명)',
            data: welfareData,
            borderColor: '#F59E0B',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            yAxisID: 'y1'
          },
          {
            label: '버스정류장수 (개)',
            data: busData,
            borderColor: '#8B5CF6',
            backgroundColor: 'rgba(139, 92, 246, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: { size: 12, weight: '500' },
              color: '#374151',
              usePointStyle: true,
              padding: 15
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#374151',
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true,
            callbacks: {
              label: function(context) {
                const value = context.parsed.y
                const label = context.dataset.label
                
                if (label.includes('면적')) {
                  return `${label}: ${value.toFixed(2)}`
                } else {
                  return `${label}: ${value.toLocaleString()}`
                }
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#6B7280',
              font: { size: 10 },
              maxRotation: 45
            }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: '면적 (km²)',
              color: '#10B981',
              font: { size: 11, weight: 'bold' }
            },
            ticks: {
              color: '#10B981',
              font: { size: 10 },
              callback: function(value) {
                return value.toFixed(1)
              }
            },
            grid: { color: '#F3F4F6' }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: '수량 (명/개)',
              color: '#F59E0B',
              font: { size: 11, weight: 'bold' }
            },
            ticks: {
              color: '#F59E0B',
              font: { size: 10 },
              callback: function(value) {
                return value.toLocaleString()
              }
            },
            grid: { drawOnChartArea: false }
          }
        }
      }
    })
  } catch (error) {
    console.error('복지 라인 차트 생성 오류:', error)
  }
}

// drawWelfareBarChart 함수 수정 (기존 함수 교체)
const drawWelfareBarChart = async (Chart) => {
  // query3에서만 실행되도록 제한
  if (result.value?.queryType !== 3) {
    console.log('welfareBarChart는 query3에서만 그립니다.')
    return
  }

  // Canvas ref가 존재하는지 먼저 확인
  if (!welfareBarChart.value) {
    console.warn('welfareBarChart ref가 존재하지 않습니다. DOM에 렌더링되지 않았을 수 있습니다.')
    return
  }

  // Canvas 준비 상태 확인
  const canvasReady = await waitForCanvasReady(welfareBarChart, 'WelfareBarChart')
  if (!canvasReady) {
    console.warn('welfareBarChart canvas가 준비되지 않았습니다')
    return
  }

  // 기존 차트 정리
  if (currentWelfareBarChart) {
    currentWelfareBarChart.destroy()
    currentWelfareBarChart = null
  }

  try {
    const ctx = welfareBarChart.value.getContext('2d')
    
    // 데이터 소스 결정
    let regions = []
    if (result.value.data?.welfare_analysis?.regions?.length) {
      regions = result.value.data.welfare_analysis.regions.slice(0, 10)
      console.log('백엔드 처리 데이터로 바 차트 생성:', regions.length, '개 지역')
    } else if (result.value.results?.length) {
      regions = result.value.results.slice(0, 10)
      console.log('원본 SPARQL 결과로 바 차트 생성:', regions.length, '개 지역')
    } else {
      console.warn('바 차트용 데이터가 없습니다')
      return
    }

    const labels = regions.map(r => {
      const name = r.지역명 || r.region || '알 수 없음'
      return String(name).length > 8 ? String(name).substring(0, 8) + '...' : String(name)
    })
    
    // 테이블에 표시되는 점수를 그대로 사용 (추가 정규화 없음)
    const scores = regions.map(r => {
      let score = 0
      
      // 백엔드에서 처리된 정규화점수가 있으면 우선 사용
      if (r.정규화점수 !== undefined && r.정규화점수 !== null) {
        score = parseFloat(r.정규화점수)
        console.log(`${r.지역명}: 정규화점수 사용 = ${score}`)
      }
      // 정규화점수가 없으면 종합점수 사용
      else if (r.종합점수 !== undefined && r.종합점수 !== null) {
        score = parseFloat(r.종합점수)
        console.log(`${r.지역명}: 종합점수 사용 = ${score}`)
      }
      // 둘 다 없으면 0
      else {
        score = 0
        console.log(`${r.지역명}: 점수 없음, 0으로 설정`)
      }
      
      return isNaN(score) ? 0 : score
    })
    
    // *** 중요: 추가 정규화 제거 - 백엔드에서 계산된 값 그대로 사용 ***
    const finalScores = scores
    
    console.log('최종 차트 점수 (정규화 없음):', finalScores)
    
    // 점수에 따른 색상 결정
    const colors = finalScores.map(score => {
      if (score >= 80) return '#DC2626' // 높은 취약성 - 빨간색
      if (score >= 60) return '#F59E0B' // 중간 취약성 - 주황색
      if (score >= 40) return '#10B981' // 보통 - 초록색
      return '#6B7280' // 낮은 취약성 - 회색
    })

    console.log('바 차트 데이터 확인:', {
      labels: labels,
      scores: finalScores,
      colors: colors.slice(0, 3)
    })

    currentWelfareBarChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: '복지 취약성 점수',
          data: finalScores,  // 백엔드 계산값 그대로 사용
          backgroundColor: colors,
          borderColor: colors,
          borderWidth: 2,
          borderRadius: 8,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#374151',
            borderWidth: 1,
            cornerRadius: 8,
            callbacks: {
              label: function(context) {
                const score = context.parsed.y
                let level = ''
                if (score >= 80) level = '높은 취약성'
                else if (score >= 60) level = '중간 취약성'
                else if (score >= 40) level = '보통'
                else level = '낮은 취약성'
                
                return `${context.dataset.label}: ${score.toFixed(1)}점 (${level})`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            // max 값을 동적으로 설정 (정규화점수면 100, 종합점수면 자동)
            max: finalScores.some(s => s > 100) ? undefined : 100,
            title: {
              display: true,
              text: '취약성 점수',
              color: '#374151',
              font: { size: 12, weight: 'bold' }
            },
            ticks: {
              color: '#6B7280',
              font: { size: 11 },
              callback: function(value) {
                return value.toFixed(0) + '점'
              }
            },
            grid: { color: '#F3F4F6' }
          },
          x: {
            ticks: {
              color: '#6B7280',
              font: { size: 10 },
              maxRotation: 45,
              minRotation: 0
            },
            grid: { display: false }
          }
        }
      }
    })
  } catch (error) {
    console.error('복지 바 차트 생성 오류:', error)
  }
}

const destroyWelfareCharts = () => {
  if (currentWelfareLineChart) {
    currentWelfareLineChart.destroy()
    currentWelfareLineChart = null
  }
  if (currentWelfareBarChart) {
    currentWelfareBarChart.destroy()
    currentWelfareBarChart = null
  }
}

// 고급 분석 차트 그리기 (소득과 충전소 상관관계)
const drawAdvancedChart = async (Chart) => {
  if (!chartCanvas.value) {
    console.warn('chartCanvas ref가 없습니다')
    return
  }

  // 기존 차트 정리
  if (currentChart) {
    currentChart.destroy()
    currentChart = null
  }

  try {
    const ctx = chartCanvas.value.getContext('2d')
    
    // 고급 분석 데이터 추출
    const districts = result.value.data?.districts || []
    const correlation = result.value.data?.correlation || 0
    
    if (districts.length === 0) {
      console.warn('고급 분석 데이터가 없습니다')
      return
    }

    // 상위 10개 지역만 표시
    const topDistricts = districts.slice(0, 10)
    
    const labels = topDistricts.map(d => {
      const name = d.name || '알 수 없음'
      return String(name).length > 8 ? String(name).substring(0, 8) + '...' : String(name)
    })
    
    const incomes = topDistricts.map(d => d.income || 0)
    const stations = topDistricts.map(d => d.chargerCount || 0)
    
    console.log('고급 분석 차트 데이터:', {
      labels: labels.length,
      incomes: incomes.filter(v => v > 0).length,
      stations: stations.filter(v => v > 0).length,
      correlation: correlation
    })

    currentChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: '평균소득 (만원)',
            data: incomes,
            backgroundColor: '#10B981',
            borderRadius: 8,
            borderColor: '#ffffff',
            borderWidth: 2,
            borderSkipped: false,
            yAxisID: 'y'
          },
          {
            label: '충전소 수 (개)',
            data: stations,
            backgroundColor: '#8B5CF6',
            borderRadius: 8,
            borderColor: '#ffffff',
            borderWidth: 2,
            borderSkipped: false,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: {
                size: 13,
                weight: '500'
              },
              color: '#374151',
              usePointStyle: true,
              padding: 20
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#374151',
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true,
            callbacks: {
              label: function(context) {
                const value = context.parsed.y
                const label = context.dataset.label
                
                if (label.includes('소득')) {
                  return `${label}: ${value.toLocaleString()}만원`
                } else {
                  return `${label}: ${value}개`
                }
              }
            },
            title: {
              display: true,
              text: `상관계수: ${correlation.toFixed(3)} (${correlation > 0.5 ? '강한 양의 상관관계' : correlation > 0.3 ? '중간 상관관계' : '약한 상관관계'})`,
              color: '#374151',
              font: {
                size: 14,
                weight: 'bold'
              },
              padding: 20
            }
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: '평균소득 (만원)',
              color: '#10B981',
              font: { size: 12, weight: 'bold' }
            },
            ticks: {
              color: '#10B981',
              font: { size: 11 },
              callback: function(value) {
                return value.toLocaleString() + '만원'
              }
            },
            grid: { color: '#F3F4F6' }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: '충전소 수 (개)',
              color: '#8B5CF6',
              font: { size: 12, weight: 'bold' }
            },
            ticks: {
              color: '#8B5CF6',
              font: { size: 11 },
              callback: function(value) {
                return value + '개'
              }
            },
            grid: { drawOnChartArea: false }
          },
          x: {
            ticks: {
              color: '#6B7280',
              font: { size: 10 },
              maxRotation: 45,
              minRotation: 0
            },
            grid: { display: false }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    })
  } catch (error) {
    console.error('고급 분석 차트 생성 오류:', error)
  }
}

// 2. Canvas 존재 및 준비 상태 확인 개선
const waitForCanvasReady = async (canvasRef, refName, maxAttempts = 20) => {
  let attempts = 0
  
  console.log(`waitForCanvasReady 시작: ${refName}, 현재 queryType: ${result.value?.queryType}`)
  
  while (attempts < maxAttempts) {
    // 1단계: ref가 존재하는지 확인
    if (!canvasRef.value) {
      console.log(`${refName}: Canvas ref not found (attempt ${attempts + 1})`)
      await new Promise(resolve => setTimeout(resolve, 150))
      attempts++
      continue
    }
    
    // 2단계: DOM에 실제로 마운트되었는지 확인
    if (!canvasRef.value.isConnected) {
      console.log(`${refName}: Canvas not connected to DOM (attempt ${attempts + 1})`)
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
      continue
    }
    
    // 3단계: 크기가 설정되었는지 확인
    const rect = canvasRef.value.getBoundingClientRect()
    if (rect.width === 0 || rect.height === 0) {
      console.log(`${refName}: Canvas size not ready: ${rect.width}x${rect.height} (attempt ${attempts + 1})`)
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
      continue
    }
    
    // 4단계: getContext가 가능한지 확인
    try {
      const ctx = canvasRef.value.getContext('2d')
      if (!ctx) {
        console.log(`${refName}: Cannot get 2D context (attempt ${attempts + 1})`)
        await new Promise(resolve => setTimeout(resolve, 100))
        attempts++
        continue
      }
    } catch (error) {
      console.log(`${refName}: Context error: ${error.message} (attempt ${attempts + 1})`)
      await new Promise(resolve => setTimeout(resolve, 100))
      attempts++
      continue
    }
    
    // 5단계: 추가 안정화 대기
    await new Promise(resolve => setTimeout(resolve, 50))
    
    console.log(`${refName}: Canvas ready after ${attempts + 1} attempts`)
    return true
  }
  
  console.error(`${refName}: Canvas not ready after ${maxAttempts} attempts`)
  return false
}


// 소득 분포 차트 그리기 (상위 10개, 하위 10개 분리)
// 2. 개선된 소득 차트 그리기 함수
const drawIncomeCharts = async (Chart) => {
  if (!result.value?.results?.length) {
    console.log('No results available for income charts')
    return
  }

  console.log('Starting income charts creation...')

  try {
    // 기존 차트 정리
    await destroyIncomeChartsAndWait()
    
    // 데이터 준비
    const chartData = prepareIncomeChartData()
    if (!chartData) {
      console.error('Failed to prepare chart data')
      return
    }
    
    console.log('Chart data prepared:', {
      topRegions: chartData.topRegions.length,
      bottomRegions: chartData.bottomRegions.length,
      yAxisMax: chartData.yAxisMax
    })
    
    // Canvas 요소들이 준비될 때까지 대기
    const topReady = await waitForCanvasReady(topChartCanvas, 'TopChart')
    const bottomReady = await waitForCanvasReady(bottomChartCanvas, 'BottomChart')
    
    if (!topReady || !bottomReady) {
      console.error('Canvas elements not ready for chart creation')
      
      // 재시도 로직
      console.log('Attempting retry in 500ms...')
      setTimeout(() => {
        if (result.value?.results?.length && shouldShowBarChart.value) {
          drawIncomeCharts(Chart)
        }
      }, 500)
      return
    }

    console.log('Both canvas elements ready, creating charts...')
    
    // 차트 생성을 순차적으로 처리
    await createTopChart(Chart, chartData)
    await new Promise(resolve => setTimeout(resolve, 100))
    await createBottomChart(Chart, chartData)
    
    console.log('Income charts created successfully')
    
  } catch (error) {
    console.error('Income charts creation error:', error)
    
    // 에러 발생 시 재시도
    setTimeout(() => {
      if (result.value?.results?.length && shouldShowBarChart.value) {
        console.log('Retrying chart creation after error...')
        drawIncomeCharts(Chart)
      }
    }, 1000)
  }
}


// 3. 차트 정리 및 대기 함수
const destroyIncomeChartsAndWait = async () => {
  if (currentTopChart) {
    currentTopChart.destroy()
    currentTopChart = null
  }
  if (currentBottomChart) {
    currentBottomChart.destroy()
    currentBottomChart = null
  }
  
  // DOM 정리 완료를 위한 대기
  await new Promise(resolve => setTimeout(resolve, 150))
}

// 4. 데이터 준비 함수 분리
const prepareIncomeChartData = () => {
  try {
    const sortedData = result.value.results
      .map(r => ({
        region: r.지역명 || '알 수 없음',
        income: parseInt(r.평균소득 || r.income || 0) || 0
      }))
      .filter(d => d.income > 0) // 유효한 데이터만
      .sort((a, b) => b.income - a.income)

    if (sortedData.length === 0) {
      console.warn('No valid income data available')
      return null
    }

    const maxIncome = Math.max(...sortedData.map(d => d.income))
    const yAxisMax = Math.ceil(maxIncome * 1.1)

    const topRegions = sortedData.slice(0, 10)
    const bottomRegions = sortedData.slice(-10).reverse()

    return {
      topRegions,
      bottomRegions,
      yAxisMax,
      totalDataPoints: sortedData.length
    }
  } catch (error) {
    console.error('Data preparation error:', error)
    return null
  }
}

// 5. 상위 차트 생성 함수
const createTopChart = async (Chart, chartData) => {
  if (!topChartCanvas.value) return

  const ctx = topChartCanvas.value.getContext('2d')
  if (!ctx) {
    console.error('Failed to get 2D context for top chart')
    return
  }

  // Context 상태 확인
  ctx.clearRect(0, 0, topChartCanvas.value.width, topChartCanvas.value.height)

  const commonOptions = getCommonChartOptions(chartData.yAxisMax)

  currentTopChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.topRegions.map(d => {
        const name = d.region
        return name.length > 8 ? name.substring(0, 8) + '...' : name
      }),
      datasets: [{
        label: '평균소득 (만원)',
        data: chartData.topRegions.map(d => d.income),
        backgroundColor: '#10B981',
        borderRadius: 8,
        borderColor: '#ffffff',
        borderWidth: 2,
        borderSkipped: false,
      }]
    },
    options: {
      ...commonOptions,
      plugins: {
        ...commonOptions.plugins,
        title: {
          display: false
        }
      }
    }
  })

  console.log('Top chart created successfully')
}

// 6. 하위 차트 생성 함수
const createBottomChart = async (Chart, chartData) => {
  if (!bottomChartCanvas.value) return

  const ctx = bottomChartCanvas.value.getContext('2d')
  if (!ctx) {
    console.error('Failed to get 2D context for bottom chart')
    return
  }

  // Context 상태 확인
  ctx.clearRect(0, 0, bottomChartCanvas.value.width, bottomChartCanvas.value.height)

  const commonOptions = getCommonChartOptions(chartData.yAxisMax)

  currentBottomChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.bottomRegions.map(d => {
        const name = d.region
        return name.length > 8 ? name.substring(0, 8) + '...' : name
      }),
      datasets: [{
        label: '평균소득 (만원)',
        data: chartData.bottomRegions.map(d => d.income),
        backgroundColor: '#F59E0B',
        borderRadius: 8,
        borderColor: '#ffffff',
        borderWidth: 2,
        borderSkipped: false,
      }]
    },
    options: {
      ...commonOptions,
      plugins: {
        ...commonOptions.plugins,
        title: {
          display: false
        }
      }
    }
  })

  console.log('Bottom chart created successfully')
}

// 7. 공통 차트 옵션
const getCommonChartOptions = (yAxisMax) => ({
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 1000,
    easing: 'easeOutCubic'
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#ffffff',
      bodyColor: '#ffffff',
      borderColor: '#374151',
      borderWidth: 1,
      cornerRadius: 8,
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}만원`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: yAxisMax,
      grid: {
        color: '#F3F4F6',
        drawBorder: false
      },
      ticks: {
        color: '#6B7280',
        font: { size: 11 },
        callback: function(value) {
          return value.toLocaleString() + '만원'
        }
      }
    },
    x: {
      grid: { display: false },
      ticks: {
        color: '#6B7280',
        font: { size: 10 },
        maxRotation: 45,
        minRotation: 0
      }
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  }
})


// query4 산점도 차트
const drawScatterChart = async (Chart) => {
  // query4에서만 실행되도록 제한
  if (result.value?.queryType !== 4) {
    console.log('scatterChart는 query4에서만 그립니다.')
    return
  }

  if (!chartCanvas.value) {
    console.warn('chartCanvas ref가 없습니다')
    return
  }

  // 기존 차트 정리
  if (currentChart) {
    currentChart.destroy()
    currentChart = null
  }

  try {
    const ctx = chartCanvas.value.getContext('2d')
    
    // Query 4 데이터 추출
    const districts = result.value.data?.districts || []
    const correlation = result.value.data?.correlation || {}
    
    if (districts.length === 0) {
      console.warn('산점도용 데이터가 없습니다')
      return
    }

    console.log('산점도 데이터 확인:', {
      districts: districts.length,
      correlation: correlation.coefficient,
      sampleData: districts.slice(0, 3)
    })

    // 산점도 데이터 포인트 생성
    const scatterData = districts.map(d => ({
      x: d.income || 0,           // X축: 소득
      y: d.chargerCount || 0,     // Y축: 충전소 수 (백엔드 필드명과 일치)
      label: d.name || '알 수 없음'
    })).filter(point => point.x > 0 && point.y > 0) // 유효한 데이터만

    console.log('산점도 포인트:', scatterData.slice(0, 3))

    // 추세선 계산
    let trendlineData = []
    if (scatterData.length > 1) {
      const x = scatterData.map(d => d.x)
      const y = scatterData.map(d => d.y)
      
      const n = x.length
      const meanX = x.reduce((a, b) => a + b, 0) / n
      const meanY = y.reduce((a, b) => a + b, 0) / n
      
      let numerator = 0
      let denominator = 0
      
      for (let i = 0; i < n; i++) {
        numerator += (x[i] - meanX) * (y[i] - meanY)
        denominator += (x[i] - meanX) ** 2
      }
      
      if (denominator !== 0) {
        const slope = numerator / denominator
        const intercept = meanY - slope * meanX
        
        const minX = Math.min(...x)
        const maxX = Math.max(...x)
        
        trendlineData = [
          { x: minX, y: slope * minX + intercept },
          { x: maxX, y: slope * maxX + intercept }
        ]
        
        console.log('추세선 계산 완료:', { slope, intercept, points: trendlineData })
      }
    }

    // 차트 생성
    const datasets = [
      {
        label: '지역별 소득-충전소 분포',
        data: scatterData,
        backgroundColor: 'rgba(99, 102, 241, 0.7)',
        borderColor: 'rgba(99, 102, 241, 1)',
        pointRadius: 8,
        pointHoverRadius: 12,
        pointBorderWidth: 2,
        pointBorderColor: '#ffffff'
      }
    ]

    // 추세선이 있으면 추가
    if (trendlineData.length > 0) {
      datasets.push({
        type: 'line',
        label: `추세선 (r=${(correlation.coefficient || 0).toFixed(3)})`,
        data: trendlineData,
        borderColor: '#EF4444', // 빨간색으로 변경
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderWidth: 4, // 기존 3에서 4로 증가
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0,
        tension: 0,
        order: 1
      })
    }

    currentChart = new Chart(ctx, {
      type: 'scatter',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1.5,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              font: { size: 12, weight: '500' },
              color: '#374151',
              usePointStyle: true,
              padding: 15
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#374151',
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true,
            callbacks: {
              title: function(context) {
                if (context.length > 0) {
                  const point = context[0].raw
                  return point.label || '지역'
                }
                return ''
              },
              label: function(context) {
                const point = context.raw
                if (context.dataset.label.includes('추세선')) {
                  return null // 추세선 툴팁은 숨김
                }
                return [
                  `평균소득: ${point.x.toLocaleString()}만원`,
                  `충전소 수: ${point.y}개`
                ]
              },
              afterBody: function() {
                const corr = correlation.coefficient || 0
                const strength = correlation.strength || '알 수 없음'
                return `\n상관계수: ${corr.toFixed(3)} (${strength})`
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: '평균소득 (만원)',
              color: '#374151',
              font: { size: 13, weight: 'bold' }
            },
            ticks: {
              color: '#6B7280',
              font: { size: 11 },
              callback: function(value) {
                return value.toLocaleString() + '만원'
              }
            },
            grid: { color: '#F3F4F6' }
          },
          y: {
            title: {
              display: true,
              text: '전기차 충전소 수 (개)',
              color: '#374151',
              font: { size: 13, weight: 'bold' }
            },
              max: 200,
              ticks: {
                color: '#6B7280',
                font: { size: 11 },
                stepSize: 50, // 한 칸의 크기를 50으로 설정
                callback: function(value) {
                  return value + '개'
                }
              },
              grid: { color: '#F3F4F6' }
          }
        },
        interaction: {
          intersect: false,
          mode: 'point'
        }
      }
    })

    console.log('산점도 차트 생성 완료')

  } catch (error) {
    console.error('산점도 차트 생성 오류:', error)
  }
}

// 결과가 변경될 때마다 차트 다시 그리기
watch(() => result.value?.results, async (newResults) => {
  if (newResults?.length) {
    await nextTick()
    await drawChart()
  }
})

// 복지 차트 타입이 변경될 때마다 차트 다시 그리기
watch(() => welfareChartType.value, async (newType) => {
  if (result.value?.queryType === 3 && result.value?.results?.length) {
    // 차트가 이미 그려져 있으므로 타입 변경만 처리
    console.log(`복지 차트 타입 변경: ${newType}`)
  }
})

const drawMap = async () => {
  destroyCharts()
  
  // DOM이 완전히 렌더링될 때까지 기다림
  await nextTick()
  
  // mapContainer가 준비될 때까지 기다림
  let attempts = 0
  while (!mapContainer.value && attempts < 10) {
    await new Promise(resolve => setTimeout(resolve, 100))
    attempts++
  }
  
  if (!mapContainer.value) {
    console.log('Map container not ready after 10 attempts')
    return
  }

  try {
    const L = await import('leaflet')
    
    // Leaflet CSS도 동적으로 로드
    if (!document.querySelector('link[href*="leaflet"]')) {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }

    // SVG 아이콘 생성 함수
    const createSVGIcon = (color = '#4F46E5') => {
      const svgString = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" fill="${color}" stroke="white" stroke-width="2"/>
          <circle cx="12" cy="9" r="2.5" fill="white"/>
        </svg>
      `
      
      return L.divIcon({
        html: svgString,
        className: 'custom-svg-icon',
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
      })
    }

    // CSS 스타일 추가 (그림자 효과)
    if (!document.querySelector('#leaflet-svg-styles')) {
      const style = document.createElement('style')
      style.id = 'leaflet-svg-styles'
      style.textContent = `
        .custom-svg-icon {
          background: none !important;
          border: none !important;
          filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        }
      `
      document.head.appendChild(style)
    }

    // 첫 번째 충전소 위치를 중심으로 지도 생성
    const firstStation = result.value.results[2]
    const centerLat = parseFloat(firstStation.위도) || 37.5665
    const centerLng = parseFloat(firstStation.경도) || 126.9780

    currentMap = L.map(mapContainer.value).setView([centerLat, centerLng], 13)

    // 기본 스타일로 OpenStreetMap 사용
    const selectedStyle = mapStyleOptions.openstreetmap
    currentTileLayer = L.tileLayer(selectedStyle.url, {
      attribution: selectedStyle.attribution
    }).addTo(currentMap)

    // 충전소 마커 추가
    let markerCount = 0
    result.value.results.forEach((station, index) => {
      const lat = parseFloat(station.위도)
      const lng = parseFloat(station.경도)
      
      if (!isNaN(lat) && !isNaN(lng)) {
        const iconColor = '#4F46E5'
        const customIcon = createSVGIcon(iconColor)
        
        const marker = L.marker([lat, lng], { icon: customIcon }).addTo(currentMap)
        markerCount++
        
        // 팝업 내용 생성
        const popupContent = `
          <div class="p-2">
            <h3 class="font-bold text-sm mb-1">${station.충전소명 || '충전소'}</h3>
            <p class="text-xs text-gray-600 mb-1">${station.주소 || '주소 정보 없음'}</p>
          </div>
        `
        
        marker.bindPopup(popupContent)
      }
    })

    console.log(`Added ${markerCount} markers to map`)

  } catch (error) {
    console.error('Map creation error:', error)
  }
}

// 복지(3) 분석 실행 및 결과 반영 함수
const onClickExecuteAdvancedQuery = async () => {
  if (loading.value) return
  
  // 사용자 쿼리도 업데이트
  userQuery.value = '지역별 소득과 전기차 충전소 개수의 상관관계를 분석해줘'
  
  loading.value = true
  destroyCharts()
  
  // 고급 분석 진행 상태 설정 (query4 - 소득과 충전소 상관관계)
  complexReasoningProgress.value = {
    isActive: true,
    currentStep: 0,
    totalSteps: 4,
    stepTitle: '',
    stepDescription: ''
  }

  try {
    await simulateAdvancedReasoningSteps()

    const response = await fetch(`${API_BASE_URL}/query/analyze/advanced`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: '지역별 소득과 전기차 충전소 개수의 상관관계를 분석해줘',
        queryType: 4
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    result.value = {
      success: data.success,
      queryType: data.queryType,
      sparqlQuery: data.sparqlQuery,
      data: data.data,
      results: data.results,
      analysis: data.analysis,
      keywords: data.keywords || [],
      reasoningSteps: generateAdvancedReasoningSteps(),
      error: data.success ? null : data.message
    }

    if (data.success && data.results?.length) {
      await nextTick()
      await drawChart()
    }

  } catch (err) {
    console.error('고급 분석 실행 오류:', err)
    result.value = {
      success: false,
      error: `고급 분석 중 오류가 발생했습니다: ${err.message}`
    }
  } finally {
    loading.value = false
    complexReasoningProgress.value.isActive = false
  }
}


// 컴포넌트 언마운트 시 차트 정리
onUnmounted(() => {
  stopTipSlider()
  destroyCharts()
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.prose {
  line-height: 1.6;
}

.prose strong {
  font-weight: 600;
  color: #374151;
}
</style>