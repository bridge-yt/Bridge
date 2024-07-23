import React, { useState } from 'react';
import { addResource } from '../api';
import { TextField, Button } from '@mui/material';

const ResourceForm = ({ namespace }) => {
  const [form, setForm] = useState({ name: '', arn: '', resource_type: '', value: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addResource(namespace, form).then(() => {
      setForm({ name: '', arn: '', resource_type: '', value: '' });
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField name="name" label="Name" value={form.name} onChange={handleChange} fullWidth margin="normal" />
      <TextField name="arn" label="ARN" value={form.arn} onChange={handleChange} fullWidth margin="normal" />
      <TextField name="resource_type" label="Resource Type" value={form.resource_type} onChange={handleChange} fullWidth margin="normal" />
      <TextField name="value" label="Value" value={form.value} onChange={handleChange} fullWidth margin="normal" />
      <Button type="submit" variant="contained" color="primary">Add Resource</Button>
    </form>
  );
};

export default ResourceForm;
