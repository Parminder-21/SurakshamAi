package com.example.surakshamai.models

import com.google.gson.annotations.SerializedName

data class AnalyzeUrlRequest(
    val url: String,
    @SerializedName("user_id")
    val userId: String? = null,
)
