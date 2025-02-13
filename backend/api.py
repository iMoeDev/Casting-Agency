from flask import Flask, jsonify, request,abort
from backend.models import db,Actor,Movie,setup_db
from flask_cors import CORS
from backend.auth.auth import  requires_auth, verify_decode_jwt, AuthError

def create_app(test_config=None):
        app = Flask(__name__)
        app.debug = True
        if test_config:
         app.config.update(test_config) 
        setup_db(app)
        CORS(app, resources={r"/api/*": {"origins": '*'}})


        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

        @app.route('/api/actors',methods=['GET'])
        @requires_auth('view:actors')
        def getActors(payload):
            actors = Actor.query.all()
            return jsonify({
            'success':True
            ,'actors':[{
            'id':actor.id,
            'name':actor.name,
            'age': actor.age,
            'gender': actor.gender
            } for actor in actors]
            })


        # GET /movies
        @app.route('/api/movies',methods=['GET'])
        @requires_auth('view:movies')
        def getMovies(payload):
            movies = Movie.query.all()
            return jsonify({
            'success':True
            ,'movies':[{
            'id':movie.id,
            'title':movie.title,
            'release_date': movie.release_date,
            } for movie in movies]
            })




        # POST /actors
        @app.route('/api/actors',methods=['POST'])
        @requires_auth('add:actors')
        def AddActors(payload):
            try:
                body = request.get_json()
                # Get data from request body
                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')    

                # Make sure required fields are provided
                if not name or not age or not gender:
                    return jsonify({
                        'success': False,
                        'error': 'Missing required fields'
                    }), 400
                

                # Create new actor
                new_actor = Actor(
                    name=name,
                    age=age,
                    gender=gender
                )
                
                # Add to database
                new_actor.insert()
               

                return jsonify({
                        'success': True,
                        'created': new_actor.id,
                        'actor':{
                            'id': new_actor.id,
                            'name':new_actor.name,
                            'age':new_actor.age,
                            'gender':new_actor.gender
                        }
                    }), 201
            
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 422
            
            finally:
                db.session.close()

        # POST /movies
        @app.route('/api/movies',methods=['POST'])
        @requires_auth('add:movies')
        def AddMovies(payload):
            try:
                body = request.get_json()
                title1 = body.get('title')
                release_date1 = body.get('release_date')

                if not title1 or not release_date1:
                    return jsonify({
                        'success':False,
                        'message':'parameter missing'
                    }),401
                new_movie = Movie(title=title1,release_date=release_date1)
            
                new_movie.insert()
                
                
                return jsonify({
                    'success':True,
                        'movie':{
                        'id':new_movie.id,  
                        'title': new_movie.title,
                        'release_date':new_movie.release_date
                        }}),201
            
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 422

            finally:
                db.session.close()

        # Update /actors
        @app.route('/api/actors/<int:actor_id>',methods=['PATCH'])
        @requires_auth('patch:actors')
        def UpdateActor(payload,actor_id):
            try:
                actor = Actor.query.get(actor_id)
                body = request.get_json()

                if not actor:
                    return jsonify({
                        'success': False,
                        'message': "Actor not found"
                    }), 404

        # Only update fields that are present in the request
                if 'name' in body and body['name'].strip():
                    actor.name = body['name']
                    actor.update()
                if 'age' in body and str(body['age']).strip():
                    actor.age = body['age']
                    actor.update()
                if 'gender' in body and body['gender'].strip():
                    actor.gender = body['gender']
                    actor.update()

                

                return jsonify({
                    'success':True,
                        'actor':{
                            'id': actor.id,
                            'name':actor.name,
                            'age':actor.age,
                            'gender':actor.gender
                        }
                        }),201

            except Exception as e:
                db.session.rollback()
                return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 401
            finally:
                db.session.close()


        # Update /movies
        @app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
        @requires_auth('patch:movies')
        def UpdateMovies(payload,movie_id):
            try:
                movie = Movie.query.get(movie_id)

                if not movie:
                    return jsonify({
                        'success': False,
                        'message': "Movie not found"
                    }), 404

                body = request.get_json()

                # Update only if field is provided AND not empty
                if 'title' in body and body['title'].strip():
                    movie.title = body['title']
                    movie.update()
                if 'release_date' in body and str(body['release_date']).strip():
                    movie.release_date = body['release_date']
                    movie.update()


                return jsonify({
                    'success': True,
                    'movie': {
                        'id': movie.id,
                        'title': movie.title,
                        'release_date': movie.release_date
                    }
                }), 200  # ✅ 200 OK for updates

            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500  # ✅ 500 for internal server errors

            finally:
                db.session.close()


        # DELETE /actors
        @app.route('/api/actors/<int:actor_id>',methods=['DELETE'])
        @requires_auth('delete:actors')
        def DeleteActor(payload,actor_id):
            try:
                actor = Actor.query.get(actor_id)

                if not actor:
                    return jsonify({
                        'success': False,
                        'message': 'Actor not found'
                    }), 404

                actor.delete()
     

                return jsonify({
                    'success': True,
                    'id': actor_id,
                    'message': f'Actor {actor_id} is successfully deleted!'
                }), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 422
            finally:
                db.session.close()
        

        # DELETE /movies
        @app.route('/api/movies/<int:movie_id>',methods=['DELETE'])
        @requires_auth('delete:movies')
        def DeleteMovies(payload,movie_id):
            try:
                movie = Movie.query.get(movie_id)

                if not movie:
                    return jsonify({
                        'success': False,
                        'message': 'Movie not found'
                    }), 404
                
                movie.delete()

                return jsonify({
                    'success': True,
                    'id': movie_id,
                    'message': f'Movie {movie_id} is successfully deleted!'
                }), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({
                        'success': False,
                        'error': str(e)
                    }), 422
            finally:
                db.session.close()



        @app.route("/api/user-info",methods=['GET'])
        def get_user_info():
            token = request.headers.get("Authorization", "").split("Bearer ")[-1]
            try:
                user_data = verify_decode_jwt(token)
                return jsonify(user_data)
            except AuthError as e:
                return jsonify(e.error), e.success_code



        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({'success': False, 'error': 400, 'message': 'Bad request - Invalid input data'}), 400

        @app.errorhandler(401)
        def unauthorized(error):
            return jsonify({'success': False, 'error': 401, 'message': 'Unauthorized - Authentication required'}), 401

        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'success': False, 'error': 404, 'message': 'Resource not found'}), 404

        @app.errorhandler(422)
        def unprocessable(error):
            return jsonify({'success': False, 'error': 422, 'message': 'Unprocessable entity - Unable to process request'}), 422


        @app.errorhandler(500)
        def server_error(error):
            return jsonify({'success': False, 'error': 500, 'message': 'Internal server error - Please try again later'}), 500


        return app


if __name__ == '__main__':
    app = create_app()
    if app: 
        app.run(debug=True)
    else:
        print("ERROR: `create_app()` returned None!")