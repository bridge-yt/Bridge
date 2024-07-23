import React, { useState } from 'react';
import { Box, Button, TextField, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';

const ResourceForm = ({ namespace, onAddResource }) => {
  const [open, setOpen] = useState(false);
  const [resource, setResource] = useState({
    name: '',
    arn: '',
    value: '',
    resource_type: '',
  });

  const handleChange = (e) => {
    setResource({ ...resource, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    onAddResource(resource);
    setOpen(false);
    setResource({
      name: '',
      arn: '',
      value: '',
      resource_type: '',
    });
  };

  return (
    <Box sx={{ textAlign: 'right', marginBottom: 2 }}>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setOpen(true)}
        sx={{ minWidth: '150px' }} // Ensure the button has a minimum width
      >
        Add Resource
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Add Resource</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Fill in the details for the new resource.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            name="name"
            label="Name"
            fullWidth
            value={resource.name}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="arn"
            label="ARN"
            fullWidth
            value={resource.arn}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="value"
            label="Value"
            fullWidth
            value={resource.value}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="resource_type"
            label="Resource Type"
            fullWidth
            value={resource.resource_type}
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)} color="primary">
            Cancel
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ResourceForm;
