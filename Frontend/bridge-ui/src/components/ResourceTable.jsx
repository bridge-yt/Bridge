import React, { useState } from 'react';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { deleteResource, updateResource } from '../api';
import {
  Box,
  Typography,
  IconButton,
  Tooltip,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
} from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const StyledDataGrid = styled(DataGrid)(({ theme }) => ({
  border: 'none',
  boxShadow: 'none',
  borderRadius: '8px',
  '& .MuiDataGrid-cell': {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  '& .MuiDataGrid-columnHeaderTitle': {
    fontWeight: 'bold',
  },
  '& .MuiDataGrid-row:hover': {
    backgroundColor: theme.palette.action.hover,
  },
  '& .MuiDataGrid-row.Mui-selected': {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
  },
  height: '100%',
  width: '100%',
}));

const ResourceTable = ({ namespace, resources, setResources }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedResource, setEditedResource] = useState(null);
  const [error, setError] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [resourceToDelete, setResourceToDelete] = useState(null);

  const handleEditClick = (params) => {
    setEditedResource(params.row);
    setIsEditing(true);
  };

  const handleCloseDialog = () => {
    setIsEditing(false);
  };

  const handleSave = async () => {
    try {
      const { id, ...resourceData } = editedResource;
      const response = await updateResource(namespace, editedResource.name, resourceData);
      setResources(resources.map(resource =>
        resource.name === editedResource.name ? response.data : resource
      ));
      setIsEditing(false);
    } catch (error) {
      setError(error);
    }
  };

  const confirmDelete = (resource) => {
    setResourceToDelete(resource);
    setIsDeleting(true);
  };

  const handleDelete = async () => {
    try {
      const response = await deleteResource(namespace, resourceToDelete.name);
      setResources(resources.filter((resource) => resource.name !== resourceToDelete.name));
      setIsDeleting(false);
      setResourceToDelete(null);
    } catch (deleteError) {
      setError(deleteError);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleting(false);
    setResourceToDelete(null);
  };

  const columns = [
    { field: 'id', headerName: 'ID', width: 150, editable: false },
    { field: 'name', headerName: 'Name', width: 200, editable: true },
    { field: 'arn', headerName: 'ARN', width: 300, editable: true },
    { field: 'resource_type', headerName: 'Resource Type', width: 200, renderCell: (params) => <Chip label={params.value} /> },
    { field: 'value', headerName: 'Value', width: 200, editable: true },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <Tooltip title="Edit">
            <IconButton onClick={() => handleEditClick(params)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton onClick={() => confirmDelete(params.row)}>
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ width: '100%', height: '100%' }}>
      {error && (
        <Typography color="error">{error.message}</Typography>
      )}
      <StyledDataGrid
        rows={resources}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 25]}
        pagination
        components={{ Toolbar: GridToolbar }}
        autoHeight
        disableExtendRowFullWidth
        sx={{
          '& .MuiDataGrid-root': {
            overflowX: 'auto',
          },
        }}
      />

      <Dialog open={isEditing} onClose={handleCloseDialog}>
        <DialogTitle>Edit Resource</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Make changes to the resource and save.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Name"
            type="text"
            fullWidth
            variant="outlined"
            value={editedResource?.name || ''}
            onChange={(e) => setEditedResource({ ...editedResource, name: e.target.value })}
          />
          <TextField
            margin="dense"
            id="arn"
            label="ARN"
            type="text"
            fullWidth
            variant="outlined"
            value={editedResource?.arn || ''}
            onChange={(e) => setEditedResource({ ...editedResource, arn: e.target.value })}
          />
          <TextField
            margin="dense"
            id="resource_type"
            label="Resource Type"
            type="text"
            fullWidth
            variant="outlined"
            value={editedResource?.resource_type || ''}
            onChange={(e) => setEditedResource({ ...editedResource, resource_type: e.target.value })}
          />
          <TextField
            margin="dense"
            id="value"
            label="Value"
            type="text"
            fullWidth
            variant="outlined"
            value={editedResource?.value || ''}
            onChange={(e) => setEditedResource({ ...editedResource, value: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSave} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={isDeleting}
        onClose={handleCancelDelete}
      >
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the resource "{resourceToDelete?.name}"?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete} color="primary">
            Cancel
          </Button>
          <Button onClick={handleDelete} color="primary" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ResourceTable;
