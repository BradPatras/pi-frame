import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [refreshInterval, setRefreshInterval] = useState('8');
  const [timeUnit, setTimeUnit] = useState('hours');

  useEffect(() => {
    // Fetch config from API
    fetch('/api/config')
      .then(response => response.json())
      .then(data => {
        setRefreshInterval(data.refreshInterval || '8');
        setTimeUnit(data.timeUnit || 'hours');
      })
      .catch(error => {
        console.error('Error fetching config:', error);
        // Set defaults on error
        setRefreshInterval('8');
        setTimeUnit('hours');
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Pi-Frame Configuration
        </p>
      </header>

      <div className="App-content">
        <label>
          <span>Refresh Interval:</span>
          <div className="input-group">
            <input
              type="number"
              id="refreshInterval"
              name="refreshInterval"
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(e.target.value)}
            />
            <select
              id="timeUnit"
              name="timeUnit"
              value={timeUnit}
              onChange={(e) => setTimeUnit(e.target.value)}
            >
              <option value="hours">hours</option>
              <option value="minutes">minutes</option>
            </select>
          </div>
        </label>
      </div>
    </div>
  );
}

export default App;
