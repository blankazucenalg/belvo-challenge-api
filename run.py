from belvo_transactions import create_app
import os

from dotenv import load_dotenv
load_dotenv()


def main():
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    app.run('0.0.0.0', port=port, threaded=True)


if __name__ == "__main__":
    main()
