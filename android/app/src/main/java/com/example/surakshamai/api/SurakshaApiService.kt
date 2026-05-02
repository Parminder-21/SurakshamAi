package com.example.surakshamai.api

import com.example.surakshamai.models.AnalyzeCallRequest
import com.example.surakshamai.models.AnalyzeMessageRequest
import com.example.surakshamai.models.AnalyzeUrlRequest
import com.example.surakshamai.models.RiskAnalysisResponse
import retrofit2.http.Body
import retrofit2.http.POST

interface SurakshaApiService {
    @POST("/analyze-message")
    suspend fun analyzeMessage(
        @Body request: AnalyzeMessageRequest,
    ): RiskAnalysisResponse

    @POST("/analyze-url")
    suspend fun analyzeUrl(
        @Body request: AnalyzeUrlRequest,
    ): RiskAnalysisResponse

    @POST("/analyze-call")
    suspend fun analyzeCall(
        @Body request: AnalyzeCallRequest,
    ): RiskAnalysisResponse
}
