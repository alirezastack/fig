from fig.fig_app import FigApp

if __name__ == '__main__':
    app = FigApp().setup()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
