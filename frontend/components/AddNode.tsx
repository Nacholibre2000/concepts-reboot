import React, { useState } from 'react';
import axios from 'axios';

const AddNode: React.FC = () => {
  const [formData, setFormData] = useState({
    image_url: '',
    concept: '',
    person: '',
    event: '',
    place_name: '',
    explanation: '',
    place_geo: '',
    date: '',
    source: '',
    license: '',
    hashtags: '', // Assuming hashtags are input as a comma-separated string
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8080/add_node', {
        ...formData,
        hashtags: formData.hashtags
          .split(',')
          .map((tag) => ({ concept: tag.trim() })), // Assuming hashtags are only concepts
      });
      alert(`Node added successfully: ${response.data.uid}`);
    } catch (error: any) {
      alert(
        `Failed to add node: ${error.response ? error.response.data.message : error.message}`,
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="image_url">Image URL:</label>
        <input
          type="text"
          id="image_url"
          name="image_url"
          value={formData.image_url}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="concept">Concept:</label>
        <input
          type="text"
          id="concept"
          name="concept"
          value={formData.concept}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="person">Person:</label>
        <input
          type="text"
          id="person"
          name="person"
          value={formData.person}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="event">Event:</label>
        <input
          type="text"
          id="event"
          name="event"
          value={formData.event}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="place_name">Place Name:</label>
        <input
          type="text"
          id="place_name"
          name="place_name"
          value={formData.place_name}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="explanation">Explanation:</label>
        <textarea
          id="explanation"
          name="explanation"
          value={formData.explanation}
          onChange={handleChange}
        ></textarea>
      </div>
      <div>
        <label htmlFor="place_geo">Place Geo (GeoJSON):</label>
        <textarea
          id="place_geo"
          name="place_geo"
          value={formData.place_geo}
          onChange={handleChange}
        ></textarea>
      </div>
      <div>
        <label htmlFor="date">Date:</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="source">Source:</label>
        <input
          type="text"
          id="source"
          name="source"
          value={formData.source}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="license">License:</label>
        <input
          type="text"
          id="license"
          name="license"
          value={formData.license}
          onChange={handleChange}
        />
      </div>
      <div>
        <label htmlFor="hashtags">Hashtags (comma-separated):</label>
        <input
          type="text"
          id="hashtags"
          name="hashtags"
          value={formData.hashtags}
          onChange={handleChange}
        />
      </div>
      <button type="submit">Add Node</button>
    </form>
  );
};

export default AddNode;
