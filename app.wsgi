import subprocess

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])

    # Ruta al script start.sh
    script_path = '/var/www/html/lamaria/docker/start.sh'

    try:
        # Ejecutar el script start.sh
        output = subprocess.check_output(['bash', script_path], stderr=subprocess.STDOUT, text=True)
        return [f"Script ejecutado correctamente:\n{output}"]
    except subprocess.CalledProcessError as e:
        # Manejar errores en la ejecución del script
        return [f"Error al ejecutar el script:\n{e.output}"]