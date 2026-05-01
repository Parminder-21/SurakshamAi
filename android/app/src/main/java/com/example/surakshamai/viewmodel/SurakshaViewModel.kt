package com.example.surakshamai.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.surakshamai.models.RiskAnalysisResponse
import com.example.surakshamai.repository.SurakshaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class SurakshaUiState(
    val isLoading: Boolean = false,
    val result: RiskAnalysisResponse? = null,
    val errorMessage: String? = null,
)

class SurakshaViewModel(
    private val repository: SurakshaRepository = SurakshaRepository(),
) : ViewModel() {

    private val _uiState = MutableStateFlow(SurakshaUiState())
    val uiState: StateFlow<SurakshaUiState> = _uiState.asStateFlow()

    fun analyzeMessage(messageText: String, userId: String? = null) {
        viewModelScope.launch {
            _uiState.value = SurakshaUiState(isLoading = true)

            repository.analyzeMessage(messageText, userId)
                .onSuccess { response ->
                    _uiState.value = SurakshaUiState(result = response)
                }
                .onFailure { error ->
                    _uiState.value = SurakshaUiState(errorMessage = error.message ?: "Something went wrong")
                }
        }
    }

    fun analyzeUrl(urlText: String, userId: String? = null) {
        viewModelScope.launch {
            _uiState.value = SurakshaUiState(isLoading = true)

            repository.analyzeUrl(urlText, userId)
                .onSuccess { response ->
                    _uiState.value = SurakshaUiState(result = response)
                }
                .onFailure { error ->
                    _uiState.value = SurakshaUiState(errorMessage = error.message ?: "Something went wrong")
                }
        }
    }

    fun clearState() {
        _uiState.value = SurakshaUiState()
    }
}
