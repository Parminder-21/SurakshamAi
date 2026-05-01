package com.example.surakshamai.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.surakshamai.viewmodel.AnalysisUiState
import com.example.surakshamai.viewmodel.AnalysisViewModel

@Composable
fun SurakshaNavGraph(
    viewModel: AnalysisViewModel = viewModel(),
) {
    val navController = rememberNavController()
    val uiState by viewModel.uiState.collectAsState()

    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(
                viewModel = viewModel,
            ) {
                navController.navigate("result")
            }
        }
        composable("result") {
            when (val state = uiState) {
                is AnalysisUiState.Success -> {
                    ResultScreen(
                        result = state.result,
                        onBackClick = {
                            viewModel.resetState()
                            navController.popBackStack()
                        }
                    )
                }
                else -> {
                    // Fallback or navigate back if state is not success
                    navController.popBackStack()
                }
            }
        }
    }
}
