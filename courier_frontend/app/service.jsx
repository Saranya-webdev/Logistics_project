const API_URL = 'http://127.0.0.1:8000/thisaiapi';

export const fetchCustomersData = async () => {
  const response = await fetch(`${API_URL}/customers/customerprofilelist/`);
  if (!response.ok) {
    throw new Error('Failed to fetch customers data');
  }
  return response.json();
};

export const fetchBookingsData = async (email = null) => {
  const url = email ? `${API_URL}/bookings/allbookingslist/?email=${encodeURIComponent(email)}` : `${API_URL}/bookings/allbookingslist/`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Failed to fetch bookings data');
  }
  return response.json();
};

export const fetchGraphsData = async () => {
  const response = await fetch(`${API_URL}/graphs`);
  if (!response.ok) {
    throw new Error('Failed to fetch graphs data');
  }
  return response.json();
};

export const fetchAgentProfile = async () => {
  const response = await fetch(`${API_URL}/agents/agentsprofilelist/`);
  if (!response.ok) {
    throw new Error('Failed to fetch agent profile');
  }
  return response.json();
};

export const fetchAgentBookings = async (email) => {
  const response = await fetch(`${API_URL}/agents/${encodeURIComponent(email)}/bookings/`);
  if (!response.ok) {
    throw new Error('Failed to fetch agent bookings');
  }
  return response.json();
};