package com.example.surakshamai.data

data class RiskAnalysisResult(
    val category: String,
    val riskScore: Double,
    val severity: String, // "safe", "suspicious", "high_risk"
    val reasons: List<String>,
    val guidance: List<String>
)
