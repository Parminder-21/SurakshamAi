package com.example.surakshamai.models

import com.google.gson.annotations.SerializedName

data class AnalyzeMessageRequest(
    val message: String,
    @SerializedName("user_id")
    val userId: String? = null,
)
