import json
import subprocess
import tempfile
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def execute_code(request):
    try:
        data = request.data
        code = data.get('code')
        language = data.get('language')

        if not code:
            return Response({'output': 'No code provided'}, status=400)

        if language != 'python':
            return Response({'output': 'Only Python is supported in this MVP'}, status=400)

        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            # Execute the code using subprocess
            result = subprocess.run(
                ['python3', temp_file_path],
                capture_output=True,
                text=True,
                timeout=5  # 5 seconds timeout
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Execution timed out (5s limit)"
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

        return Response({'output': output})

    except Exception as e:
        return Response({'output': f"Server Error: {str(e)}"}, status=500)
