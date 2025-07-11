import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';

function Header() {
  return (
    <AppBar position="static" color="primary" elevation={2}>
      <Toolbar>
        <Box display="flex" alignItems="center" gap={2}>
          <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f4c8.png" alt="Logo" width={36} height={36} />
          <Typography variant="h6" fontWeight={700} color="inherit">
            AI-Powered Resume Analyzer
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
