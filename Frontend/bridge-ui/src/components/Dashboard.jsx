import React, { useState, useEffect } from 'react';
import {
  Box, Typography, List, ListItemButton, ListItemText, ListItemIcon, CircularProgress, TextField, InputAdornment,
  Card, CardContent, Grid, Fade, Toolbar, AppBar, Divider, Button
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import FolderIcon from '@mui/icons-material/Folder';
import ResourceTable from './ResourceTable';
import ResourceForm from './ResourceForm';
import NamespaceForm from './NamespaceForm';
import { getNamespaces, getResources, addResource, createNamespace } from '../api';

const Dashboard = () => {
  const [namespaces, setNamespaces] = useState([]);
  const [selectedNamespace, setSelectedNamespace] = useState('');
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchNamespaces = async () => {
      try {
        const response = await getNamespaces();
        setNamespaces(response.data.namespaces);
        setSelectedNamespace(response.data.namespaces[0]);
      } catch (error) {
        console.error('Error fetching namespaces:', error);
        setError(error);
      }
    };

    fetchNamespaces();
  }, []);

  useEffect(() => {
    const fetchResources = async () => {
      if (!selectedNamespace) return;
      setLoading(true);
      try {
        const response = await getResources(selectedNamespace);
        setResources(response.data.resources);
      } catch (error) {
        console.error('Error fetching resources:', error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchResources();
  }, [selectedNamespace]);

  const handleNamespaceClick = (namespace) => {
    setSelectedNamespace(namespace);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleAddResource = async (resource) => {
    try {
      const response = await addResource(selectedNamespace, resource);
      setResources([...resources, response.data]);
    } catch (error) {
      console.error('Error adding resource:', error);
      setError(error);
    }
  };

  const handleAddNamespace = async (namespace) => {
    try {
      const response = await createNamespace(namespace);
      setNamespaces([...namespaces, namespace]);
      setSelectedNamespace(namespace);
    } catch (error) {
      console.error('Error adding namespace:', error);
      setError(error);
    }
  };

  const filteredResources = resources.filter((resource) =>
    resource.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Box sx={{ padding: 3, minHeight: '100vh', backgroundColor: '#f4f6f8' }}>
      <AppBar position="static" className="MuiAppBar-root">
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Resource Management
          </Typography>
          <TextField
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Search..."
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ width: '300px' }}
          />
        </Toolbar>
      </AppBar>

      <Grid container spacing={3} alignItems="stretch" justifyContent="center" sx={{ mt: 2 }}>
        <Grid item xs={12} md={3}>
          <Card className="MuiCard-root">
            <CardContent>
              <Typography variant="h6" align="center" gutterBottom>
                Namespaces
              </Typography>
              <Divider />
              <List>
                {namespaces.map((ns) => (
                  <ListItemButton
                    key={ns}
                    onClick={() => handleNamespaceClick(ns)}
                    selected={ns === selectedNamespace}
                    sx={{
                      borderRadius: 1,
                      '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.04)' },
                    }}
                  >
                    <ListItemIcon>
                      <FolderIcon sx={{ color: 'inherit' }} />
                    </ListItemIcon>
                    <ListItemText primary={ns} primaryTypographyProps={{ color: 'textPrimary' }} />
                  </ListItemButton>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={9}>
          <Box display="flex" justifyContent="flex-end" mb={2} gap={2}>
            <NamespaceForm onAddNamespace={handleAddNamespace} />
            <ResourceForm namespace={selectedNamespace} onAddResource={handleAddResource} />
          </Box>
          {loading ? (
            <Box display="flex" justifyContent="center" alignItems="center" height="100%">
              <CircularProgress color="primary" />
            </Box>
          ) : error ? (
            <Typography variant="h6" color="error" align="center">
              {error.message}
            </Typography>
          ) : (
            <Fade in={!!selectedNamespace} timeout={500}>
              <Box>
                <Typography variant="h5" gutterBottom>
                  Namespace: {selectedNamespace}
                </Typography>
                <ResourceTable
                  namespace={selectedNamespace}
                  resources={filteredResources}
                  setResources={setResources}
                />
              </Box>
            </Fade>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
