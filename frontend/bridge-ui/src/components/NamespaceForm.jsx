import React, { useState } from 'react';
import { Box, Button, TextField, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';

const NamespaceForm = ({ onAddNamespace }) => {
  const [open, setOpen] = useState(false);
  const [namespace, setNamespace] = useState('');

  const handleChange = (e) => {
    setNamespace(e.target.value);
  };

  const handleSubmit = () => {
    onAddNamespace(namespace);
    setOpen(false);
    setNamespace('');
  };

  return (
    <Box sx={{ textAlign: 'right', marginBottom: 2 }}>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setOpen(true)}
        sx={{ minWidth: '150px' }} // Ensure the button has a minimum width
      >
        Add Namespace
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Add Namespace</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the name for the new namespace.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            name="namespace"
            label="Namespace"
            fullWidth
            value={namespace}
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

export default NamespaceForm;
