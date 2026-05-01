package com.example.surakshamai.data

import kotlinx.coroutines.delay

class RiskAnalysisRepository {
    suspend fun analyzeThreat(message: String, url: String): RiskAnalysisResult {
        // Simulate network delay
        delay(2000)
        
        // Mock logic to simulate backend response
        return if (url.contains("scam") || message.lowercase().contains("lottery")) {
            RiskAnalysisResult(
                category = "PHISHING_ATTEMPT",
                riskScore = 88.5,
                severity = "high_risk",
                reasons = listOf("Known malicious domain", "Urgent/Winning language detected"),
                guidance = listOf("Do not click any links", "Report this message as spam", "Block the sender immediately")
            )
        } else {
            RiskAnalysisResult(
                category = "GENERAL_COMMUNICATION",
                riskScore = 12.0,
                severity = "safe",
                reasons = listOf("No suspicious patterns detected", "Domain has good reputation"),
                guidance = listOf("Safe to interact", "Always remain cautious with unknown senders")
            )
        }
    }
}
