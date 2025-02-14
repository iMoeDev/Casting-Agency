import React, { useState, useEffect,useCallback } from 'react';
import './Agency.css'
import {useAuth0} from '@auth0/auth0-react'

const Agency = () => {
  const [movies, setMovies] = useState([]);
  const [actors, setActors] = useState([]);
  const [error, setError] = useState(null);
  const [showAddMovie, setShowAddMovie] = useState(false);
  const [showAddActor, setShowAddActor] = useState(false);
  const [newMovie, setNewMovie] = useState({ title: '', release_date: '' });
  const [newActor, setNewActor] = useState({ name: '', age: '', gender: '' });
  const { loginWithPopup, logout, getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [editingActor, setEditingActor] = useState(false);
  const [editingMovie,setEditingMovie] = useState(false)
  const [permissions, setPermissions] = useState([]); 
  const [token, setToken] = useState(localStorage.getItem("token"));
  let body='';


  
  const fetchUserInfo = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/user-info", {
        headers: { Authorization: `Bearer ${token}` },
      });
  
      if (!response.ok) throw new Error("Failed to fetch user info");
  
      const userData = await response.json();
  
      if (userData?.permissions) {
        setPermissions(userData.permissions);
      } else {
        console.error("Permissions not found in userData");
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  };
  
  const fetchData = useCallback(
    async (endpoint) => {
      try {
        if (!token) {
          console.warn("No token found - User might not be logged in.");
          return [];
        }
  
        const response = await fetch(`http://127.0.0.1:5000/api/${endpoint}`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
  
        if (response.status === 401) {
          throw new Error("Unauthorized - Please log in again");
        }
  
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
  
        return await response.json();
      } catch (err) {
        console.error(`Error fetching ${endpoint}:`, err);
        return [];
      }
    },
    [token]
  );
  
  useEffect(() => {
    const fetchAllData = async () => {
      if (!token) return;
  
      if (permissions.length === 0) {
        await fetchUserInfo();
      }
  
      const promises = [];
  
      if (permissions.includes("view:movies") && movies.length === 0) {
        promises.push(fetchData("movies").then((data) => setMovies(data.movies || [])));
      }
  
      if (permissions.includes("view:actors") && actors.length === 0) {
        promises.push(fetchData("actors").then((data) => setActors(data.actors || [])));
      }
  
      await Promise.all(promises);
    };
  
    fetchAllData();
  }, [fetchData, permissions, token]);
  
  const handleLogin = async () => {
    try {
      await loginWithPopup({ authorizationParams: { prompt: "login" } });
  
      const newToken = await getAccessTokenSilently();
      localStorage.setItem("token", newToken);
      setToken(newToken);
  
      await fetchUserInfo(); 
    } catch (error) {
      console.error("Login error:", error);
    }
  };

const handleLogout= async()=>{
  localStorage.removeItem('token', localStorage.getItem('token'));
  await logout({
    logoutParams: {
      returnTo: window.location.origin,
    }
  });  window.location.reload();

}


const handleAddMovie = async () => {
    fetch('http://127.0.0.1:5000/api/movies', {
      method: 'POST',
      headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(newMovie)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
          console.log("movie insert data: ", data.movie);
          // Add the single movie object to the existing movies
          setMovies(prevMovies => [...prevMovies, data.movie]);
          setShowAddMovie(false);
          setNewMovie({ title: '', release_date: ''});
        }
    })
    .catch(err => {
        console.error('Error:', err);
        setError('Failed to add Movie');
    });
};


  const handleAddActor = () => {
    fetch('http://127.0.0.1:5000/api/actors', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newActor)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            setActors(prevActors => [...prevActors, {
                id: data.actor.id,
                name: data.actor.name,
                age: data.actor.age,
                gender: data.actor.gender
            }]);
            setShowAddActor(false);
            setNewActor({ name: '', age: '', gender: '' });
        }
    })
    .catch(err => {
        console.error('Error:', err);
        setError('Failed to add actor');
    });
};


const handleDelete = async (id, type) => {
  console.log(id)
  console.log(type)
  fetch(`http://127.0.0.1:5000/api/${type}/${id}`, { 
      method: 'DELETE',
      headers: {
          'Authorization': `Bearer ${token}`
      }
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`Failed to delete ${type.slice(0, -1)}`);
      }
      return response.json();
  })
  .then( res => {
      if (type === 'movies') {
        setMovies(prevMovies => prevMovies.filter(movie => movie.id !== res.id));
      } else {
        console.log('here',id)
        setActors(prevActors => prevActors.filter(actor => actor.id !== res.id));
        console.log(actors)
      }
  })
  .catch(err => {
      console.error(err);
      setError(err.message);
  });
};


  const handleUpdate= async (id, type) =>{
    console.log(id)
    console.log(type)
    
    if (type === 'movies'){
     body = JSON.stringify({
      title: newMovie.title,
      release_date: newMovie.release_date
     })
     console.log('the movie body: ',body)
    }
    else if (type === 'actors') { 
      body = JSON.stringify({
        name: newActor.name,
        age: newActor.age,
        gender: newActor.gender
      });
      console.log('Actor update body:', body);
    }
    fetch(`http://127.0.0.1:5000/api/${type}/${id}`, { 
      method: 'PATCH',

      body:body
      ,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`Failed to update ${type.slice(0, -1)}`);
      }
      return response.json();
  })
  .then(res => {
    if (type === 'movies') {
      setMovies(prevMovies => 
        prevMovies.map(movie => 
          movie.id === res.movie.id ? res.movie : movie
        )
      );
      setNewMovie({ title: '', release_date: '' })
      setEditingMovie(false)
    } else {
      setActors(prevActors => 
        prevActors.map(actor => 
          actor.id === res.actor.id ? res.actor : actor
        )
      );
      setNewActor({ name: '', age: '', gender: '' })
      setEditingActor(false)
    }


  })
  .catch(err => {
      console.error(err);
      console.log('hey there is an errorr!!')
      setError(err.message);
  });




  }




  return (
    <div className="container mx-auto p-4">
              <h1 className="text-2xl font-bold">Casting Agency</h1>

              <nav>
     {!isAuthenticated ? (
       <button onClick={handleLogin}>Login</button>
     ) : (
       <button onClick={handleLogout}>Logout</button>
     )}
   </nav>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Movies</h2>
          <button 
            className="px-4 py-2 bg-green-500 text-white rounded"
            onClick={() => setShowAddMovie(true)}
            disabled={!permissions.includes("add:movies")}

          >
            Add Movie
          </button>
        </div>

        {showAddMovie && (
          <div >
            <div >
              <h3 >Add New Movie</h3>
              <input
                placeholder="Title"
                value={newMovie.title}
                onChange={(e) => setNewMovie({...newMovie, title: e.target.value})}
              />
              <input
                type="date"
                value={newMovie.release_date}
                onChange={(e) => setNewMovie({...newMovie, release_date: e.target.value})}
              />
              <div >
                <button 
                
                  onClick={() => setShowAddMovie(false)}
                >
                  Cancel
                </button>
                <button 
                  className="px-4 py-2 bg-blue-500 text-white rounded"
                  onClick={handleAddMovie}

                >
                  Add
                </button>
              </div>
            </div>
          </div>
        )}

<table className="w-full">
  <thead>
    <tr>
      <th className="text-left p-2">Title</th>
      <th className="text-left p-2">Release Date</th>
      <th className="text-left p-2">Actions</th>
    </tr>
  </thead>
  <tbody>
  { movies.map((movie) => (
    <tr key={movie.id} className="border-t">
      {editingMovie === movie.id ? ( 
        <>
          <td className="p-2">
            <input
              type="text"
              defaultValue={movie.title}
              className="border p-1 rounded"
              onChange={(e) =>
                setNewMovie((prev) => ({ ...prev, title: e.target.value }))
              }
            />
          </td>
          <td className="p-2">
            <input
              type="date"
              defaultValue= {new Date(movie.release_date).toISOString().split("T")[0]}
              className="border p-1 rounded"
              onChange={(e) =>
                setNewMovie((prev) => ({ ...prev, release_date: e.target.value }))
              }
            />
          </td>
        </>
      ) : (
        <>
          <td className="p-2">{movie.title}</td>
          <td className="p-2"> {new Date(movie.release_date).toISOString().split("T")[0]}</td>
        </>
      )}

      <td className="p-2">
        {editingMovie !== movie.id ? (
          <>
            <button
              className="px-3 py-1 bg-blue-500 text-white rounded mr-2"
              disabled={!permissions.includes("patch:movies")}

              onClick={() => {
                setEditingMovie(movie.id); // Set the movie being edited
                setNewMovie({ title: movie.title, release_date: movie.release_date }); 
                
              }}
            >
              Edit
            </button>
            <button
              className="px-3 py-1 bg-red-500 text-white rounded"
              onClick={() => handleDelete(movie.id, "movies")}
              disabled={!permissions.includes("delete:movies")}

            >
              Delete
            </button>
          </>
        ) : (
          <>
            <button
              className="px-4 py-2 bg-gray-500 text-white rounded mr-2"
              onClick={() => setEditingMovie(null)} 
            >
              Cancel
            </button>
            <button
              className="px-3 py-1 bg-blue-500 text-white rounded"
              onClick={() => {
                handleUpdate(movie.id, "movies");
                setEditingMovie(null); 
              }}
            >
              Submit
            </button>
          </>
        )}
      </td>
    </tr>
  ))}
</tbody>

</table>
      </div>

      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Actors</h2>
          <button 
            className="px-4 py-2 bg-green-500 text-white rounded"
            onClick={() => setShowAddActor(true)}
            disabled={!permissions.includes("add:actors")}

          >
            Add Actor
          </button>
        </div>

        {showAddActor && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-6 rounded-lg">
              <h3 className="text-lg font-bold mb-4">Add New Actor</h3>
              <input
                className="w-full p-2 mb-4 border rounded"
                placeholder="Name"
                value={newActor.name}
                onChange={(e) => setNewActor({...newActor, name: e.target.value})}
              />
              <input
                className="w-full p-2 mb-4 border rounded"
                type="number"
                placeholder="Age"
                value={newActor.age}
                onChange={(e) => setNewActor({...newActor, age: e.target.value})}
              />
                <select
                  className="w-full p-2 mb-4 border rounded"
                  value={newActor.gender}
                  onChange={(e) => setNewActor({ ...newActor, gender: e.target.value })}
                >
                  <option value="" disabled>Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              <div className="flex justify-end gap-2">
                <button 
                  className="px-4 py-2 bg-gray-500 text-white rounded"
                  onClick={() => setShowAddActor(false)}
                >
                  Cancel
                </button>

                <button 
                  className="px-4 py-2 bg-blue-500 text-white rounded"
                  onClick={handleAddActor}
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        )}



        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">Name</th>
              <th className="text-left p-2">Age</th>
              <th className="text-left p-2">Gender</th>
              <th className="text-left p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
  {actors.map((actor) => (
    <tr key={actor.id} className="border-t">
      {editingActor === actor.id ? ( 
        <>
          <td className="p-2">
            <input
              type="text"
              defaultValue={actor.name}
              className="border p-1 rounded"
              onChange={(e) =>
                setNewActor((prev) => ({ ...prev, name: e.target.value }))
              }
            />
          </td>
          <td className="p-2">
            <input
              type="number"
              defaultValue={actor.age}
              className="border p-1 rounded"
              onChange={(e) =>
                setNewActor((prev) => ({ ...prev, age: e.target.value }))
              }
            />
          </td>
          <td className="p-2">
          <select
            className="w-full p-2 mb-4 border rounded"
            value={newActor.gender}
            onChange={(e) => setNewActor({ ...newActor, gender: e.target.value })}
          >
            <option value="" disabled>Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
          </td>
        </>
      ) : (
        <>
          <td className="p-2">{actor.name}</td>
          <td className="p-2">{actor.age}</td>
          <td className="p-2">{actor.gender}</td>
        </>
      )}

      <td className="p-2">
        {editingActor !== actor.id ? (
          <>
            <button
              className="px-3 py-1 bg-blue-500 text-white rounded mr-2"
              disabled={!permissions.includes("patch:actors")}
              onClick={() => {
                setEditingActor(actor.id); 
                setNewActor({ name: actor.name, age: actor.age, gender: actor.gender }); 
              }}
            >
              Edit
            </button>
            <button
              className="px-3 py-1 bg-red-500 text-white rounded"
              disabled={!permissions.includes("delete:actors")}
              onClick={() => handleDelete(actor.id, "actors")}
            >
              Delete
            </button>
          </>
        ) : (
          <>
            <button
              className="px-4 py-2 bg-gray-500 text-white rounded mr-2"
              onClick={() => setEditingActor(null)} 
            >
              Cancel
            </button>
            <button
              className="px-3 py-1 bg-blue-500 text-white rounded"
              onClick={() => {
                handleUpdate(actor.id, "actors");
                setEditingActor(null); 
              }}
            >
              Submit
            </button>
          </>
        )}
      </td>
    </tr>
  ))}
</tbody>

        </table>
      </div>
    </div>
  );
};

export default Agency;