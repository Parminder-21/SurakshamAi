package com.example.surakshamai.ui

import androidx.compose.animation.Crossfade
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.Message
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.filled.Security
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.surakshamai.ui.theme.SurakshamAiTheme
import com.example.surakshamai.viewmodel.AnalysisUiState
import com.example.surakshamai.viewmodel.AnalysisViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: AnalysisViewModel = viewModel(),
    onNavigateToResult: () -> Unit = {}
) {
    var selectedTabIndex by remember { mutableStateOf(0) }
    var inputText by remember { mutableStateOf("") }
    
    val uiState by viewModel.uiState.collectAsState()

    // Navigate when success
    LaunchedEffect(uiState) {
        if (uiState is AnalysisUiState.Success) {
            onNavigateToResult()
        }
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Default.Security,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(28.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "Suraksha Agent",
                            fontWeight = FontWeight.Bold,
                            fontSize = 20.sp
                        )
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "Shielding you from scams",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(24.dp))

            // Tab Navigation
            val tabs = listOf("Message", "URL", "Call")
            val icons = listOf(Icons.Default.Message, Icons.Default.Link, Icons.Default.Phone)
            
            TabRow(
                selectedTabIndex = selectedTabIndex,
                containerColor = MaterialTheme.colorScheme.surface,
                contentColor = MaterialTheme.colorScheme.primary,
                divider = {} // Remove default divider
            ) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTabIndex == index,
                        onClick = { 
                            selectedTabIndex = index 
                            inputText = "" // Clear input when switching tabs
                            viewModel.resetState()
                        },
                        text = { Text(title, fontWeight = FontWeight.Bold) },
                        icon = { Icon(icons[index], contentDescription = null) }
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Input Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                )
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Crossfade(targetState = selectedTabIndex, label = "TabContent") { tabIndex ->
                        when(tabIndex) {
                            0 -> {
                                OutlinedTextField(
                                    value = inputText,
                                    onValueChange = { inputText = it },
                                    label = { Text("Paste Suspicious Message") },
                                    placeholder = { Text("e.g. Your KYC is expiring today. Click here to update...") },
                                    leadingIcon = { Icon(Icons.Default.Message, contentDescription = null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(16.dp),
                                    minLines = 4,
                                    maxLines = 6
                                )
                            }
                            1 -> {
                                OutlinedTextField(
                                    value = inputText,
                                    onValueChange = { inputText = it },
                                    label = { Text("Paste URL / Link") },
                                    placeholder = { Text("e.g. http://scam-site.com") },
                                    leadingIcon = { Icon(Icons.Default.Link, contentDescription = null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(16.dp),
                                    singleLine = true
                                )
                            }
                            2 -> {
                                OutlinedTextField(
                                    value = inputText,
                                    onValueChange = { inputText = it },
                                    label = { Text("Paste Call Transcript / Summary") },
                                    placeholder = { Text("e.g. Caller claimed to be from Police and demanded money...") },
                                    leadingIcon = { Icon(Icons.Default.Phone, contentDescription = null) },
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(16.dp),
                                    minLines = 4,
                                    maxLines = 6
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(8.dp))

                    // Error Message
                    if (uiState is AnalysisUiState.Error) {
                        Text(
                            text = (uiState as AnalysisUiState.Error).message,
                            color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall,
                            modifier = Modifier.padding(horizontal = 4.dp)
                        )
                    }

                    // Analyze Button
                    Button(
                        onClick = { 
                            when(selectedTabIndex) {
                                0 -> viewModel.analyzeMessage(inputText)
                                1 -> viewModel.analyzeUrl(inputText)
                                2 -> viewModel.analyzeCall(inputText)
                            }
                        },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp),
                        shape = RoundedCornerShape(16.dp),
                        enabled = inputText.isNotBlank() && uiState !is AnalysisUiState.Loading
                    ) {
                        if (uiState is AnalysisUiState.Loading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(24.dp),
                                color = MaterialTheme.colorScheme.onPrimary,
                                strokeWidth = 2.dp
                            )
                        } else {
                            Text("Analyze Threat", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Info Section
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.Info,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = "Suraksha Agent uses local-first AI to ensure your data stays private.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun HomeScreenPreview() {
    SurakshamAiTheme {
        HomeScreen()
    }
}
