package com.example.surakshamai.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.surakshamai.data.RiskAnalysisResult
import com.example.surakshamai.ui.theme.SurakshamAiTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResultScreen(
    result: RiskAnalysisResult,
    onBackClick: () -> Unit = {}
) {
    // Standard Material 3 Colors
    val severityColor = when (result.severity.lowercase()) {
        "safe" -> Color(0xFF4CAF50)
        "suspicious" -> Color(0xFFFFC107)
        "high_risk" -> Color(0xFFF44336)
        else -> Color.Gray
    }

    val severityIcon = when (result.severity.lowercase()) {
        "safe" -> Icons.Default.CheckCircle
        "suspicious" -> Icons.Default.Warning
        "high_risk" -> Icons.Default.Error
        else -> Icons.Default.Info
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Analysis Result", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(imageVector = Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(16.dp))

            // Main Result Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(
                    containerColor = severityColor.copy(alpha = 0.1f)
                ),
                border = BorderStroke(1.dp, severityColor)
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        imageVector = severityIcon,
                        contentDescription = null,
                        tint = severityColor,
                        modifier = Modifier.size(64.dp)
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    Text(
                        text = result.category.uppercase().replace("_", " "),
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold,
                        color = severityColor
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    Surface(
                        color = severityColor,
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(
                            text = result.severity.uppercase().replace("_", " "),
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                            color = Color.White,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    Spacer(modifier = Modifier.height(20.dp))

                    Row(verticalAlignment = Alignment.Bottom) {
                        Text(
                            text = result.riskScore.toString(),
                            fontSize = 48.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Text(
                            text = "/100",
                            fontSize = 18.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(bottom = 10.dp, start = 4.dp)
                        )
                    }
                    Text(
                        text = "Risk Score",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Reasons
            Text(
                text = "Analysis Reasons",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)
            )
            
            result.reasons.forEach { reason ->
                Card(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                    shape = RoundedCornerShape(12.dp),
                    border = BorderStroke(0.5.dp, severityColor.copy(alpha = 0.3f))
                ) {
                    Text(
                        text = reason,
                        modifier = Modifier.padding(16.dp),
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Guidance
            Text(
                text = "Preventive Actions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)
            )
            
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    result.guidance.forEach { step ->
                        Row(modifier = Modifier.padding(vertical = 4.dp)) {
                            Text("• ", fontWeight = FontWeight.Bold)
                            Text(text = step, style = MaterialTheme.typography.bodyMedium, lineHeight = 20.sp)
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(40.dp))
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ResultScreenPreview() {
    SurakshamAiTheme {
        ResultScreen(
            result = RiskAnalysisResult(
                category = "lottery_scam",
                riskScore = 85.0,
                severity = "high_risk",
                reasons = listOf("Urgent language", "Request for money"),
                guidance = listOf("Block sender", "Do not share OTP")
            )
        )
    }
}
