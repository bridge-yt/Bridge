import React, { useEffect, useState } from 'react';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { getResources, deleteResource } from '../api';
import { Button } from '@mui/material';

const columns = [
  { field: 'id', headerName: 'ID', width: 150 },
  { field: 'name', headerName: 'Name', width: 200 },
  { field: 'arn', headerName: 'ARN', width: 300 },
  { field: 'resource_type', headerName: 'Resource Type', width: 200 },
  {
    field: 'actions',
    headerName: 'Actions',
    width: 150,
    renderCell: (params) => (
      <Button
        variant="contained"
        color="secondary"
        onClick={() => handleDelete(params.row.id)}
      >
        Delete
      </Button>
    ),
  },
];

const ResourceTable = ({ namespace }) => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true; // Flag to track component mounting status

    const fetchResources = async () => {
      try {
        console.log('Fetching resources for namespace:', namespace);
        const response = await getResources(namespace);
        if (isMounted) { // Check if component is still mounted before updating state
          setResources(response.data.resources);
          console.log('Resources fetched:', response.data.resources);
        }
      } catch (error) {
        console.error('Error fetching resources:', error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchResources();

    return () => {
      isMounted = false; // Component unmounting
      console.log('Component unmounted');
    };
  }, [namespace]); // Include namespace as a dependency

  const handleDelete = async (id) => {
    try {
      console.log('Deleting resource with ID:', id);
      await deleteResource(namespace, id);
      setResources(resources.filter(resource => resource.id !== id));
      console.log('Resource deleted successfully');
    } catch (error) {
      setError(error);
      console.error('Error deleting resource:', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={resources}
        columns={columns}
        pageSize={5}
        checkboxSelection
        components={{
          Toolbar: GridToolbar, // Add toolbar for search, filter, etc.
        }}
      />
    </div>
  );
};

export default ResourceTable;
