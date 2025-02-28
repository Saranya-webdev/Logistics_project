import React, { useState, useEffect } from 'react';
import { FaCrown, FaSearch } from 'react-icons/fa';
import PropTypes from 'prop-types';

const EntityList = ({ endpoint, entityType, onEntityClick }) => {
  const [entities, setEntities] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchEntities() {
      try {
        setLoading(true);
        const response = await fetch(endpoint);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched data from API:', data);

        if (!Array.isArray(data)) {
          console.error("Expected an array but got:", data);
          return;
        }

        // Sort entities alphabetically by name
        const sortedEntities = data
          .filter(entity => entity && entity[`${entityType}_name`]) // Prevent undefined values
          .sort((a, b) => (a[`${entityType}_name`] || "").localeCompare(b[`${entityType}_name`] || ""));

        setEntities(sortedEntities);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }
    fetchEntities();
  }, [endpoint, entityType]);

  if (loading) {
    return <div className="text-center text-gray-500">Loading {entityType}...</div>;
  }

  if (error) {
    return (
      <div className="text-center text-red-600 bg-red-100 p-2 rounded-md">
        Failed to fetch {entityType}: {error}
      </div>
    );
  }

  if (!entities.length) {
    return <div className="text-center text-gray-600">No {entityType.toLowerCase()} available</div>;
  }

  const filteredEntities = entities.filter(
    (entity) =>
      entity[`${entityType}_name`] &&
      entity[`${entityType}_name`].toLowerCase().includes(searchTerm.toLowerCase())
  );

  console.log('Filtered entities:', filteredEntities);
  console.log("Entities before filtering:", entities);
  console.log("Search term:", searchTerm);

  return (
    <div className="max-w-sm mx-auto lg:w-[70%] h-[100%] p-4 bg-[#F1F4F7] rounded-lg flex flex-col md:w-[50%] gap-4 items-center">
      {/* Sticky Search Bar */}
      <div className="w-full bg-[#F1F4F7]  sticky top-0">
        <div className="flex items-center px-4 mb-4 h-12 w-full bg-white rounded-md ">
          <FaSearch className="text-gray-700 text-xl mr-2" />
          <input
            type="text"
            placeholder={`Search ${entityType}`}
            className="flex-grow p-2 outline-none rounded-md"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>
  
      {/* Scrollable Entity List */}
      <div className="w-full h-[700px] overflow-y-auto no-scrollbar">
        {filteredEntities.length === 0 ? (
          <div className="text-center text-gray-600">No {entityType.toLowerCase()} available</div>
        ) : (
          <ul className="entity w-full flex flex-col gap-2">
            {filteredEntities.map((entity) => (
              <EntityItem key={entity[`${entityType}_id`]} entity={entity} entityType={entityType} onClick={() => onEntityClick(entity)} />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
  
};

EntityList.propTypes = {
  endpoint: PropTypes.string.isRequired,
  entityType: PropTypes.string.isRequired,
  onEntityClick: PropTypes.func.isRequired,
};

const EntityItem = ({ entity, entityType, onClick }) => (
  <li className="flex items-start px-4 py-3 border rounded-lg bg-white shadow-sm cursor-pointer" onClick={onClick}>
    <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
    <div className="flex-1">
      <div className="text-gray-900 text-[1rem] font-bold font-Inria">{entity[`${entityType}_name`]}</div>
      <div className="text-[#718096] text-[1rem] font-normal font-Mono">{entity[`${entityType}_mobile`]}</div>
      <div className="text-[#718096] text-[1rem] font-normal font-Mono">{entity[`${entityType}_email`]}</div>
    </div>
    {entity[`${entityType}_category`] === 'tier_1' && <FaCrown className="text-[#4972b4] text-xl" />}
  </li>
);

EntityItem.propTypes = {
  entity: PropTypes.object.isRequired,
  entityType: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default EntityList;


// for service.jsx's entitylist

// import React, { useState, useEffect } from 'react';
// import { FaCrown, FaSearch } from 'react-icons/fa';
// import PropTypes from 'prop-types';

// const EntityList = ({ endpoint, entityType, onEntityClick }) => {
//   const [entities, setEntities] = useState([]);
//   const [searchTerm, setSearchTerm] = useState('');
//   const [error, setError] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     async function fetchEntities() {
//       try {
//         setLoading(true);
//         console.log(`Fetching data from endpoint: ${endpoint}`);
//         const response = await fetch(endpoint);
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         console.log('Fetched data from API:', data);

//         if (!Array.isArray(data)) {
//           console.error("Expected an array but got:", data);
//           return;
//         }

//         // Sort entities alphabetically by name
//         const sortedEntities = data
//           .filter(entity => entity && entity[`${entityType}_name`]) // Prevent undefined values
//           .sort((a, b) => (a[`${entityType}_name`] || "").localeCompare(b[`${entityType}_name`] || ""));

//         setEntities(sortedEntities);
//       } catch (error) {
//         console.error('Error fetching entities:', error);
//         setError(error.message);
//       } finally {
//         setLoading(false);
//       }
//     }
//     fetchEntities();
//   }, [endpoint, entityType]);

//   if (loading) {
//     return <div className="text-center text-gray-500">Loading {entityType}...</div>;
//   }

//   if (error) {
//     return (
//       <div className="text-center text-red-600 bg-red-100 p-2 rounded-md">
//         Failed to fetch {entityType}: {error}
//       </div>
//     );
//   }

//   if (!entities.length) {
//     return <div className="text-center text-gray-600">No {entityType.toLowerCase()} available</div>;
//   }

//   const filteredEntities = entities.filter(
//     (entity) =>
//       entity[`${entityType}_name`] &&
//       entity[`${entityType}_name`].toLowerCase().includes(searchTerm.toLowerCase())
//   );

//   console.log('Filtered entities:', filteredEntities);
//   console.log("Entities before filtering:", entities);
//   console.log("Search term:", searchTerm);

//   return (
//     <div className="max-w-sm mx-auto lg:w-[70%] h-[100%] p-4 bg-[#F1F4F7] rounded-lg flex flex-col md:w-[50%] gap-4 items-center">
//       {/* Sticky Search Bar */}
//       <div className="w-full bg-[#F1F4F7] z-10 sticky top-0">
//         <div className="flex items-center px-4 mb-4 h-12 w-full bg-white rounded-md shadow-md">
//           <FaSearch className="text-gray-700 text-xl mr-2" />
//           <input
//             type="text"
//             placeholder={`Search ${entityType}`}
//             className="flex-grow p-2 outline-none rounded-md"
//             value={searchTerm}
//             onChange={(e) => setSearchTerm(e.target.value)}
//           />
//         </div>
//       </div>
  
//       {/* Scrollable Entity List */}
//       <div className="w-full h-[700px] overflow-y-auto no-scrollbar">
//         {filteredEntities.length === 0 ? (
//           <div className="text-center text-gray-600">No {entityType.toLowerCase()} available</div>
//         ) : (
//           <ul className="entity w-full flex flex-col gap-2">
//             {filteredEntities.map((entity) => (
//               <EntityItem key={entity[`${entityType}_id`]} entity={entity} entityType={entityType} onClick={() => onEntityClick(entity)} />
//             ))}
//           </ul>
//         )}
//       </div>
//     </div>
//   );
// };

// EntityList.propTypes = {
//   endpoint: PropTypes.string.isRequired,
//   entityType: PropTypes.string.isRequired,
//   onEntityClick: PropTypes.func.isRequired,
// };

// const EntityItem = ({ entity, entityType, onClick }) => (
//   <li className="flex items-start px-4 py-3 border rounded-lg bg-white shadow-sm cursor-pointer" onClick={onClick}>
//     <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
//     <div className="flex-1">
//       <div className="text-gray-900 text-[1rem] font-bold font-Inria">{entity[`${entityType}_name`]}</div>
//       <div className="text-[#718096] text-[1rem] font-normal font-Mono">{entity[`${entityType}_mobile`]}</div>
//       <div className="text-[#718096] text-[1rem] font-normal font-Mono">{entity[`${entityType}_email`]}</div>
//     </div>
//     {entity[`${entityType}_category`] === 'tier_1' && <FaCrown className="text-[#4972b4] text-xl" />}
//   </li>
// );

// EntityItem.propTypes = {
//   entity: PropTypes.object.isRequired,
//   entityType: PropTypes.string.isRequired,
//   onClick: PropTypes.func.isRequired,
// };

// export default EntityList;