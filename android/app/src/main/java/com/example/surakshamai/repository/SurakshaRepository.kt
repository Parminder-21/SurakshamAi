package com.example.surakshamai.repository

import com.example.surakshamai.api.RetrofitProvider
import com.example.surakshamai.api.SurakshaApiService
import com.example.surakshamai.models.AnalyzeMessageRequest
import com.example.surakshamai.models.AnalyzeUrlRequest
import com.example.surakshamai.models.RiskAnalysisResponse

class SurakshaRepository(
    private val apiService: SurakshaApiService = RetrofitProvider.surakshaApiService,
) {
    suspend fun analyzeMessage(
        messageText: String,
        userId: String? = null,
    ): Result<RiskAnalysisResponse> {
        return runCatching {
            apiService.analyzeMessage(
                request = AnalyzeMessageRequest(
                    message = messageText,
                    userId = userId,
                ),
            )
        }
    }

    suspend fun analyzeUrl(
        urlText: String,
        userId: String? = null,
    ): Result<RiskAnalysisResponse> {
        return runCatching {
            apiService.analyzeUrl(
                request = AnalyzeUrlRequest(
                    url = urlText,
                    userId = userId,
                ),
            )
        }
    }
}
