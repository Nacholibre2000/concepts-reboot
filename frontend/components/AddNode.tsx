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

  const [showFields, setShowFields] = useState({
    image_url: false,
    concept: false,
    person: false,
    event: false,
    place_name: false,
    explanation: false,
    place_geo: false,
    date: false,
    source: false,
    license: false,
    hashtags: false,
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

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setShowFields((prevShowFields) => {
      const newShowFields = {
        ...prevShowFields,
        [name]: checked,
        explanation: checked || prevShowFields.explanation,
        source: checked || prevShowFields.source,
        hashtags: checked || prevShowFields.hashtags,
      };

      if (name === 'image_url') {
        newShowFields.license = checked;
      }
      if (name === 'event' || name === 'person') {
        newShowFields.date = checked;
      }
      if (name === 'place_name') {
        newShowFields.place_geo = checked;
      }

      return newShowFields;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'http://localhost:5000/api/node_data/add_node',
        {
          ...formData,
          hashtags: formData.hashtags
            .split(',')
            .map((tag) => ({ concept: tag.trim() })), // Assuming hashtags are only concepts
        },
      );
      alert(`Node added successfully: ${response.data.uid}`);
    } catch (error) {
      const err = error as AxiosError; // Type assertion here
      alert(
        `Failed to add node: ${err.response ? err.response.data.message : err.message}`,
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          <input
            type="checkbox"
            name="image_url"
            checked={showFields.image_url}
            onChange={handleCheckboxChange}
          />
          Image URL
        </label>
        {showFields.image_url && (
          <div>
            <label htmlFor="image_url">Image URL:</label>
            <input
              type="text"
              id="image_url"
              name="image_url"
              value={formData.image_url}
              onChange={handleChange}
            />
            <label htmlFor="license">License:</label>
            <input
              type="text"
              id="license"
              name="license"
              value={formData.license}
              onChange={handleChange}
            />
          </div>
        )}
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            name="concept"
            checked={showFields.concept}
            onChange={handleCheckboxChange}
          />
          Concept
        </label>
        {showFields.concept && (
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
        )}
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            name="person"
            checked={showFields.person}
            onChange={handleCheckboxChange}
          />
          Person
        </label>
        {showFields.person && (
          <div>
            <label htmlFor="person">Person:</label>
            <input
              type="text"
              id="person"
              name="person"
              value={formData.person}
              onChange={handleChange}
            />
            <label htmlFor="date">Date:</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
          </div>
        )}
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            name="event"
            checked={showFields.event}
            onChange={handleCheckboxChange}
          />
          Event
        </label>
        {showFields.event && (
          <div>
            <label htmlFor="event">Event:</label>
            <input
              type="text"
              id="event"
              name="event"
              value={formData.event}
              onChange={handleChange}
            />
            <label htmlFor="date">Date:</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
          </div>
        )}
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            name="place_name"
            checked={showFields.place_name}
            onChange={handleCheckboxChange}
          />
          Place Name
        </label>
        {showFields.place_name && (
          <div>
            <label htmlFor="place_name">Place Name:</label>
            <input
              type="text"
              id="place_name"
              name="place_name"
              value={formData.place_name}
              onChange={handleChange}
            />
            <label htmlFor="place_geo">Place Geo (GeoJSON):</label>
            <textarea
              id="place_geo"
              name="place_geo"
              value={formData.place_geo}
              onChange={handleChange}
            ></textarea>
          </div>
        )}
      </div>
      {(showFields.image_url ||
        showFields.concept ||
        showFields.person ||
        showFields.event ||
        showFields.place_name) && (
        <>
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
            <label htmlFor="hashtags">Hashtags (comma-separated):</label>
            <input
              type="text"
              id="hashtags"
              name="hashtags"
              value={formData.hashtags}
              onChange={handleChange}
            />
          </div>
        </>
      )}
      <button type="submit">Add Node</button>
    </form>
  );
};

export default AddNode;
