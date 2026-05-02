package com.example.surakshamai.models

import com.google.gson.annotations.SerializedName

data class AnalyzeCallRequest(
    @SerializedName("call_summary")
    val callSummary: String,
    @SerializedName("user_id")
    val userId: String? = null
)
