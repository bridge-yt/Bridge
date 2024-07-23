import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use(request => {
  console.log('Starting Request', request);
  return request;
});

api.interceptors.response.use(response => {
  console.log('Response:', response);
  return response;
}, error => {
  console.error('Response Error:', error);
  return Promise.reject(error);
});

export const getNamespaces = async () => {
  console.log('getNamespaces: Making API call to fetch namespaces');
  try {
    const response = await api.get('/namespaces');
    console.log('getNamespaces: API response received:', response);
    return response;
  } catch (error) {
    console.error('getNamespaces: API call failed:', error);
    throw error;
  }
};

export const getResources = async (namespace) => {
  console.log(`getResources: Making API call to fetch resources for namespace: ${namespace}`);
  try {
    const response = await api.get(`/resource/${namespace}/all`);
    console.log('getResources: API response received:', response);
    console.log('getResources: API response data:', response.data);
    return response;
  } catch (error) {
    console.error('getResources: API call failed:', error);
    throw error;
  }
};

export const addResource = async (namespace, data) => {
  console.log(`addResource: Making API call to add resource to namespace: ${namespace}`, data);
  try {
    const response = await api.post(`/resource/${namespace}`, data);
    console.log('addResource: API response received:', response);
    return response;
  } catch (error) {
    console.error('addResource: API call failed:', error);
    throw error;
  }
};

export const updateResource = async (namespace, name, data) => {
  console.log(`updateResource: Making API call to update resource in namespace: ${namespace}`, data);
  try {
    const response = await api.put(`/resource/${namespace}/${name}`, data);
    console.log('updateResource: API response received:', response);
    return response;
  } catch (error) {
    console.error('updateResource: API call failed:', error);
    throw error;
  }
};

export const deleteResource = async (namespace, name) => {
  console.log(`deleteResource: Making API call to delete resource in namespace: ${namespace} with name: ${name}`);
  try {
    const response = await api.delete(`/resource/${namespace}/${name}`);
    console.log('deleteResource: API response received:', response);
    return response;
  } catch (error) {
    console.error('deleteResource: API call failed:', error);
    throw error;
  }
};

// Add the createNamespace function
export const createNamespace = async (namespace) => {
  console.log(`createNamespace: Making API call to create namespace: ${namespace}`);
  try {
    const response = await api.post('/namespace', { namespace });
    console.log('createNamespace: API response received:', response);
    return response;
  } catch (error) {
    console.error('createNamespace: API call failed:', error);
    throw error;
  }
};
