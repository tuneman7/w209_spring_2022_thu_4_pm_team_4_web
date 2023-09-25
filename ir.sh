export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
export HNSWLIB_NO_NATIVE=1  
pip install --upgrade pip
python3 -m pip install --upgrade setuptools
pip install -r requirements.txt
