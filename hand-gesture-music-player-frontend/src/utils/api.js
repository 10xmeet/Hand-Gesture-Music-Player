const BACKEND_URL = 'http://localhost:5000';

export const fetchGestureData = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/gesture-data`);
    if (!response.ok) {
      throw new Error('Failed to fetch gesture data');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching gesture data:', error);
    return {
      volume: 0,
      fingerCount: 0,
      gestureName: 'Error',
    };
  }
};