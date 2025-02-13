import unittest
import json
from api import create_app
from models import db, Actor, Movie  
import os



class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Execute before each test"""
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.getenv('DB_TEST_URL'),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        })  
        #  Ensure test client is created
        self.client = self.app.test_client


        ##  Assign Role-Based Tokens (Replace with real tokens)
        self.casting_assistant_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhkVFJ3RkJ0cUlCMUJrZGRQZ18wbCJ9.eyJpc3MiOiJodHRwczovL2Rldi1oc2QyMTB3cW5yMWNtdTRmLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FjZDdhYjJjODA1NDZiZmJjZWJhMTgiLCJhdWQiOlsiY29mZmVlIiwiaHR0cHM6Ly9kZXYtaHNkMjEwd3FucjFjbXU0Zi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM5Mzg3MjcwLCJleHAiOjE3Mzk0NzM2NzAsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYQjlOOFFTejVKczcwaEhLOWFETFZlbEViMHBDVEdiVCIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.Jxv_dZbxzlhxFwl74mWAq3bgWtY9BevHwD4ngpX6G96iTTrjcknG3Rtrn301QAyqd1DiH_QGutMjdyOBtKLk-b2qGbUGQuxcHKtIEZdg2gIooHtLlhZ5z2P_zOoDy5DdddAutIDXfwut6Kja8ed-FoAuMOdVYxae0yyYNmlTY2Guo9uxjYA8QflLF14ukCcB8xxPDeaVNKab0GCJkrBHoDSMJ2o6M_6z83Ef1ieF1n_A34-RRIDg0FM_zvaIxCnmXbpBFremQqC4ZM5zWjruxBnnaFs1wiTLUGpFmPOEmmv1VVLKzQXV5UtZUDNrcz1cjQc41asimEKWePEiWrH_Jw"
        self.casting_director_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhkVFJ3RkJ0cUlCMUJrZGRQZ18wbCJ9.eyJpc3MiOiJodHRwczovL2Rldi1oc2QyMTB3cW5yMWNtdTRmLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FjZDdjZWFiM2Y4MGE5ZDU3N2JiNzMiLCJhdWQiOlsiY29mZmVlIiwiaHR0cHM6Ly9kZXYtaHNkMjEwd3FucjFjbXU0Zi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM5NDMxMzAzLCJleHAiOjE3Mzk1MTc3MDMsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYQjlOOFFTejVKczcwaEhLOWFETFZlbEViMHBDVEdiVCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.LFptTDPIU9bt4hJDJLASP88ewpTP3ek-C95xq_3ml4zABNRMqLRzUa_8ISdmBt_lqR6vcxz29Vl2f301uqhM9UVmYkjZ5hii473CrNtKWEQ4ly6PKZYBYIKtucNsv4XHvwyrZYkd6GnKII72pHQ7tNI3XZHZ1r6D4bjozQSKwnVtsjrMwjrC9N55HhUhSM8cZsX6l3144z6Aupv-VJSdhXMVRqbZqurnc-MZ5lXYxnRyI9iKzAHC_NKlEKKKbXx9jXuKwHtAlhGiWHu5u1qs6K4A_O3xvEZ8kp4DNffj025B52FasLXnfSVL2ehshmg07mEIywVZlbiQaqzc5-SLLQ"
        self.executive_producer_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhkVFJ3RkJ0cUlCMUJrZGRQZ18wbCJ9.eyJpc3MiOiJodHRwczovL2Rldi1oc2QyMTB3cW5yMWNtdTRmLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FjZDdmM2E0YWYxZTdhYjE1OWYxMDMiLCJhdWQiOlsiY29mZmVlIiwiaHR0cHM6Ly9kZXYtaHNkMjEwd3FucjFjbXU0Zi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM5NDMxMzYyLCJleHAiOjE3Mzk1MTc3NjIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYQjlOOFFTejVKczcwaEhLOWFETFZlbEViMHBDVEdiVCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.r37i_6O2ERwbo4TE13tpOs9OJVKKTTx5J40ylQbZQD0GussX3nCHjPMwsG-tkrrFZk31SOHRin2mJJYUeGI0LWIdZLfgejru8RoTio8GDmdii-8lJ3Hf962GJhJDDxD6zitM_tv0qxhVNhdjCxfF43Uq3vepK_I3tVSASFfB-EyOeVy71w3FZEzgdigDT_UcI3aiOlbkWeJn344TNYez45IB1RXQP34xNmBC4_9yqq1h672fuHxcx10ywlS7v3CnYNKvn5z8Ka41ELmH76OWokghN_P3_yr_CpfXSDqWIDtugDQ__Y6US-7--gN7uBEz2wmDdFdDF7cnGm6nxA7yvQ"
        self.invalid_jwt = "eMoeJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhkVFJ3RkJ0cUlCMUJrZGRQZ18wbCJ9.eyJpc3MiOiJodHRwczovL2Rldi1oc2QyMTB3cW5yMWNtdTRmLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FjZDdmM2E0YWYxZTdhYjE1OWYxMDMiLCJhdWQiOlsiY29mZmVlIiwiaHR0cHM6Ly9kZXYtaHNkMjEwd3FucjFjbXU0Zi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzM5NDMxMzYyLCJleHAiOjE3Mzk1MTc3NjIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhenAiOiJYQjlOOFFTejVKczcwaEhLOWFETFZlbEViMHBDVEdiVCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.r37i_6O2ERwbo4TE13tpOs9OJVKKTTx5J40ylQbZQD0GussX3nCHjPMwsG-tkrrFZk31SOHRin2mJJYUeGI0LWIdZLfgejru8RoTio8GDmdii-8lJ3Hf962GJhJDDxD6zitM_tv0qxhVNhdjCxfF43Uq3vepK_I3tVSASFfB-EyOeVy71w3FZEzgdigDT_UcI3aiOlbkWeJn344TNYez45IB1RXQP34xNmBC4_9yqq1h672fuHxcx10ywlS7v3CnYNKvn5z8Ka41ELmH76OWokghN_P3_yr_CpfXSDqWIDtugDQ__Y6US-7--gN7uBEz2wmDdFdDF7cnGm6nxA7yvQ"

        #  Initialize database only ONCE in `create_app()`
        with self.app.app_context():
            db.create_all()



    def tearDown(self):
        """Execute after each test"""
        pass

   
     # GET /api/actors (Success - Any role)
    def test_get_actors_success(self):
        res = self.client().get('/api/actors', headers={
            "Authorization": f"Bearer {self.casting_assistant_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    ##  ERROR TEST: GET /api/actors (Invalid token)
    def test_get_actors_forbidden(self):
        res = self.client().get('/api/actors', headers={
            "Authorization": f"Bearer {self.invalid_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)  

    # Validate the error response
        self.assertFalse(data["success"])
        self.assertEqual(data["code"], "invalid_header")  
        self.assertEqual(data["description"], "Unable to parse token header.")  

    ##  POST /api/actors (Success - Casting Director)
    def test_add_actor_success(self):
        new_actor = {"name": "Jane Doe", "age": "25", "gender": "female"}
        res = self.client().post('/api/actors', json=new_actor, headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    ##  POST /api/actors (Unauthorized - Casting Assistant)
    def test_add_actor_unauthorized(self):
        new_actor = {"name": "Jane Doe", "age": "25", "gender": "female"}
        res = self.client().post('/api/actors', json=new_actor, headers={
            "Authorization": f"Bearer {self.casting_assistant_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    ##  DELETE /api/actors (Success - Casting Director)
    def test_delete_actor_success(self):
        actor = Actor(name="Delete Me", age="30", gender="male")
        with self.app.app_context():
            db.session.add(actor)
            db.session.commit()
            actor_id = actor.id
        res = self.client().delete(f'/api/actors/{actor_id}', headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    ##  DELETE /api/actors (Unauthorized - Casting Assistant)
    def test_delete_actor_unauthorized(self):
        res = self.client().delete('/api/actors/1', headers={
            "Authorization": f"Bearer {self.casting_assistant_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    ##  GET /api/movies (Success - Any role)
    def test_get_movies_success(self):
        res = self.client().get('/api/movies', headers={
            "Authorization": f"Bearer {self.casting_assistant_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    ##  GET /api/movies (No token)
    def test_get_movies_unauthorized(self):
        res = self.client().get('/api/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    ##  POST /api/movies (Success - Executive Producer)
    def test_add_movie_success(self):
        new_movie = {"title": "New Movie", "release_date": "2025-06-15"}
        res = self.client().post('/api/movies', json=new_movie, headers={
            "Authorization": f"Bearer {self.executive_producer_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    ##  POST /api/movies (Unauthorized - Casting Director)
    def test_add_movie_unauthorized(self):
        new_movie = {"title": "New Movie", "release_date": "2025-06-15"}
        res = self.client().post('/api/movies', json=new_movie, headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    ##  DELETE /api/movies (Success - Executive Producer)
    def test_delete_movie_success(self):
        movie = Movie(title="Delete Me", release_date="2023-01-01")
        with self.app.app_context():
            db.session.add(movie)
            db.session.commit()
            movie_id=movie.id
        res = self.client().delete(f'/api/movies/{movie_id}', headers={
            "Authorization": f"Bearer {self.executive_producer_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    ## DELETE /api/movies (Unauthorized - Casting Director)
    def test_delete_movie_unauthorized(self):
        res = self.client().delete('/api/movies/2', headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)


    ## PATCH /api/actors (Success - Casting Director)
    def test_update_actor_success(self):
        """Test successful update of an actor (Casting Director)"""
        with self.app.app_context():
            actor = Actor(name="Old Name", age="40", gender="male")
            db.session.add(actor)
            db.session.commit()
            actor_id = actor.id  # Store ID before session closes

        updated_data = {"name": "New Name"}
        res = self.client().patch(f'/api/actors/{actor_id}', json=updated_data, headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor"]["name"], "New Name")

    ##  PATCH /api/actors (Actor Not Found)
    def test_update_actor_not_found(self):
        """Test updating a non-existent actor"""
        non_existent_actor_id = 9999
        updated_data = {"name": "Ghost Actor"}
        
        res = self.client().patch(f'/api/actors/{non_existent_actor_id}', json=updated_data, headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Actor not found")

    ##  PATCH /api/movies (Success - Casting Director)
    def test_update_movie_success(self):
        """Test successful update of a movie (Casting Director)"""
        with self.app.app_context():
            movie = Movie(title="Old Title", release_date="2023-01-01")
            db.session.add(movie)
            db.session.commit()
            movie_id = movie.id  # Store ID before session closes

        updated_data = {"title": "New Title"}
        res = self.client().patch(f'/api/movies/{movie_id}', json=updated_data, headers={
            "Authorization": f"Bearer {self.casting_director_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"]["title"], "New Title")

    ##  PATCH /api/movies (Movie Not Found)
    def test_update_movie_not_found(self):
        """Test updating a non-existent movie"""
        non_existent_movie_id = 9999
        updated_data = {"title": "Ghost Movie"}
        
        res = self.client().patch(f'/api/movies/{non_existent_movie_id}', json=updated_data, headers={
            "Authorization": f"Bearer {self.executive_producer_jwt}"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Movie not found")



if __name__ == '__main__':
    unittest.main()