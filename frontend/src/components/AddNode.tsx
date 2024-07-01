import React, { useState } from 'react';
import axios from 'axios';
import { useSelectedItems } from '../context/SelectedItemsContext'; // Import the hook

const AddNode: React.FC = () => {
  const { selectedContentAndRequirements } = useSelectedItems(); // Use the hook
  const [formData, setFormData] = useState({
    image_url: '',
    concept: '',
    person: '',
    event: '',
    place_name: '',
    explanation: '',
    place_geo: { type: 'Point', coordinates: [0, 0] }, // Default GeoJSON structure
    date: '',  // Assuming the date is in 'YYYY-MM-DD' format
    source: '',
    license: '',
    hashtags: [] as { name: string; type: string }[], // List of hashtags with type
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
  });

  const [curriculumHashtagsAdded, setCurriculumHashtags] = useState(false);

  const [newHashtag, setNewHashtag] = useState({ name: '', type: 'concept' });

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
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

  const handleAddCurriculumHashtags = () => {
    setCurriculumHashtags(true);
  };

  const handleAddHashtag = () => {
    setFormData({
      ...formData,
      hashtags: [...formData.hashtags, { ...newHashtag }],
    });
    setNewHashtag({ name: '', type: 'concept' }); // Reset new hashtag input
  };

  const handleHashtagChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setNewHashtag({
      ...newHashtag,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const allHashtags = [
        ...formData.hashtags,
        ...(curriculumHashtagsAdded ? selectedContentAndRequirements.map(tag => ({ name: tag, type: 'curriculum' })) : [])
      ];
      
      console.log('Form data being submitted:', {
        ...formData,
        hashtags: allHashtags,
      });
      
      const response = await axios.post(
        'http://localhost:5000/api/node_data/add_node',
        {
          ...formData,
          hashtags: allHashtags,
          date: formData.date ? new Date(formData.date).toISOString() : null,
        },
      );
      alert(`Node added successfully: ${response.data.uid}`);
    } catch (error) {
      const err = error as any;
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
              value={JSON.stringify(formData.place_geo)}  // Convert GeoJSON to string for display
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
            <h4>Hashtags</h4>
            {formData.hashtags.map((tag, index) => (
              <div key={index}>
                <span>
                  {tag.name} ({tag.type})
                </span>
              </div>
            ))}
            <div>
              <input
                type="text"
                name="name"
                value={newHashtag.name}
                onChange={handleHashtagChange}
                placeholder="Hashtag name"
              />
              <select
                name="type"
                value={newHashtag.type}
                onChange={handleHashtagChange}
              >
                <option value="concept">Concept</option>
                <option value="person">Person</option>
                <option value="event">Event</option>
                <option value="place_name">Place</option>
              </select>
              <button type="button" onClick={handleAddHashtag}>
                Add Hashtag
              </button>
            </div>
            <button 
              type="button" 
              onClick={handleAddCurriculumHashtags}
              style={{ backgroundColor: curriculumHashtagsAdded ? 'green' : 'initial' }}
            >
              {curriculumHashtagsAdded ? 'Curriculum Items Added as Hashtags' : 'Add Curriculum Selection as Hashtags'}
            </button>
          </div>
        </>
      )}
      <button type="submit">Add Node</button>
    </form>
  );
};

export default AddNode;
