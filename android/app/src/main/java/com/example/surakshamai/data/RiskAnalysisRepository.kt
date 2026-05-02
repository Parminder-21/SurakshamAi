package com.example.surakshamai.data

import com.example.surakshamai.api.RetrofitProvider
import com.example.surakshamai.models.AnalyzeCallRequest
import com.example.surakshamai.models.AnalyzeMessageRequest
import com.example.surakshamai.models.AnalyzeUrlRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class RiskAnalysisRepository {
    private val api = RetrofitProvider.surakshaApiService

    suspend fun analyzeMessage(message: String): RiskAnalysisResult {
        return withContext(Dispatchers.IO) {
            val response = api.analyzeMessage(AnalyzeMessageRequest(message = message))
            mapResponse(response)
        }
    }

    suspend fun analyzeUrl(url: String): RiskAnalysisResult {
        return withContext(Dispatchers.IO) {
            val response = api.analyzeUrl(AnalyzeUrlRequest(url = url))
            mapResponse(response)
        }
    }

    suspend fun analyzeCall(callSummary: String): RiskAnalysisResult {
        return withContext(Dispatchers.IO) {
            val response = api.analyzeCall(AnalyzeCallRequest(callSummary = callSummary))
            mapResponse(response)
        }
    }

    private fun mapResponse(response: com.example.surakshamai.models.RiskAnalysisResponse): RiskAnalysisResult {
        // The backend returns guidance as a single string with bullets "- bullet".
        // Let's split it into a list for the UI.
        val guidanceList = response.advice
            .split("\n")
            .map { it.removePrefix("-").trim() }
            .filter { it.isNotEmpty() }

        return RiskAnalysisResult(
            category = response.category,
            riskScore = response.riskScore,
            severity = response.severity,
            reasons = response.reasons,
            guidance = guidanceList
        )
    }
}
