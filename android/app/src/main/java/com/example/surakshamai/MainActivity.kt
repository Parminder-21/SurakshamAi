package com.example.surakshamai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.surakshamai.ui.HomeScreen
import com.example.surakshamai.ui.theme.SurakshamAiTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            SurakshamAiTheme {
                HomeScreen()
            }
        }
    }
}