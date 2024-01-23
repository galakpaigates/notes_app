from website import create_app
import os

app = create_app()

@app.errorhandler(404)
def page_not_found(error):
    return '<h2>404, Not found!</h2>', 404

@app.errorhandler(400)
def bad_request(error):
    return '<h2>400, Bad request!</h2>', 400

@app.errorhandler(500)
def internal_server_error(error):
    return '<h2>500, Internal Server Error!</h2>', 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=os.getenv("PORT", default=5000))
