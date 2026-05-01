package com.example.surakshamai.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.surakshamai.data.RiskAnalysisRepository
import com.example.surakshamai.data.RiskAnalysisResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class AnalysisUiState {
    object Idle : AnalysisUiState()
    object Loading : AnalysisUiState()
    data class Success(val result: RiskAnalysisResult) : AnalysisUiState()
    data class Error(val message: String) : AnalysisUiState()
}

class AnalysisViewModel(private val repository: RiskAnalysisRepository = RiskAnalysisRepository()) : ViewModel() {

    private val _uiState = MutableStateFlow<AnalysisUiState>(AnalysisUiState.Idle)
    val uiState: StateFlow<AnalysisUiState> = _uiState.asStateFlow()

    fun analyze(message: String, url: String) {
        viewModelScope.launch {
            _uiState.value = AnalysisUiState.Loading
            try {
                val result = repository.analyzeThreat(message, url)
                _uiState.value = AnalysisUiState.Success(result)
            } catch (e: Exception) {
                _uiState.value = AnalysisUiState.Error(e.localizedMessage ?: "An unknown error occurred")
            }
        }
    }
    
    fun resetState() {
        _uiState.value = AnalysisUiState.Idle
    }
}
