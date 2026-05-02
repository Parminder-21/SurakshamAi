package com.example.surakshamai.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
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
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
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

    // Animation for progress bar
    var animationPlayed by remember { mutableStateOf(false) }
    val currentPercentage by animateFloatAsState(
        targetValue = if (animationPlayed) (result.riskScore / 100f).toFloat() else 0f,
        animationSpec = tween(durationMillis = 1500),
        label = "progress"
    )

    LaunchedEffect(key1 = true) {
        animationPlayed = true
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

            // Main Risk Card with Circular Progress
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(
                    containerColor = severityColor.copy(alpha = 0.05f)
                ),
                border = BorderStroke(1.dp, severityColor.copy(alpha = 0.5f))
            ) {
                Column(
                    modifier = Modifier.padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        // Circular Progress Indicator
                        CircularProgressIndicator(
                            progress = currentPercentage,
                            modifier = Modifier.size(160.dp),
                            color = severityColor,
                            strokeWidth = 12.dp,
                            strokeCap = StrokeCap.Round,
                            trackColor = MaterialTheme.colorScheme.surfaceVariant
                        )
                        
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                imageVector = severityIcon,
                                contentDescription = null,
                                tint = severityColor,
                                modifier = Modifier.size(32.dp)
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = "${(currentPercentage * 100).toInt()}",
                                fontSize = 42.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    
                    Text(
                        text = result.category.uppercase().replace("_", " "),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.ExtraBold,
                        color = severityColor,
                        textAlign = TextAlign.Center
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    Surface(
                        color = severityColor,
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(
                            text = result.severity.uppercase().replace("_", " "),
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp),
                            color = Color.White,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Reasons Section
            if (result.reasons.isNotEmpty()) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Warning, contentDescription = null, tint = severityColor)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Why we flagged this",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                result.reasons.forEach { reason ->
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                        ),
                        border = BorderStroke(0.5.dp, severityColor.copy(alpha = 0.2f))
                    ) {
                        Row(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "• ", 
                                fontWeight = FontWeight.Bold, 
                                color = severityColor
                            )
                            Text(
                                text = reason,
                                style = MaterialTheme.typography.bodyMedium
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Guidance Section
            if (result.guidance.isNotEmpty()) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Shield, contentDescription = null, tint = Color(0xFF4CAF50))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Safe Actions",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = Color(0xFF4CAF50).copy(alpha = 0.05f)
                    ),
                    border = BorderStroke(1.dp, Color(0xFF4CAF50).copy(alpha = 0.3f))
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        result.guidance.forEach { step ->
                            Row(modifier = Modifier.padding(vertical = 6.dp)) {
                                Icon(
                                    imageVector = Icons.Default.CheckCircle, 
                                    contentDescription = null, 
                                    tint = Color(0xFF4CAF50),
                                    modifier = Modifier.size(20.dp)
                                )
                                Spacer(modifier = Modifier.width(12.dp))
                                Text(
                                    text = step, 
                                    style = MaterialTheme.typography.bodyMedium, 
                                    lineHeight = 20.sp
                                )
                            }
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
                reasons = listOf("Urgent language detected in message", "Request for money or sensitive info", "Uses a shortening service link"),
                guidance = listOf("Do not click any links or download attachments", "Block the sender immediately", "Do not share OTP")
            )
        )
    }
}
