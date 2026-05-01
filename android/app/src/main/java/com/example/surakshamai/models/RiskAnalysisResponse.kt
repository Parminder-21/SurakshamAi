package com.example.surakshamai.models

import com.google.gson.annotations.SerializedName

data class RiskAnalysisResponse(
    val category: String,
    @SerializedName("risk_score")
    val riskScore: Double,
    val severity: String,
    val reasons: List<String>,
    val advice: String,
    val url: String?,
    @SerializedName("suspicious_flags")
    val suspiciousFlags: List<String>,
    @SerializedName("scrubbed_text")
    val scrubbedText: String?,
    val timestamp: String,
)
