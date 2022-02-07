# Commands executed for GCP Cloud Run deployment:

```
gcloud auth login
gcloud init
gcloud config set compute/region europe-west4
gcloud config set compute/zone europe-west4
gcloud services enable run.googleapis.com containerregistry.googleapis.com
gcloud auth configure-docker
docker tag mjs-streamlit:latest gcr.io/mjs-datavisualisation/mjs-streamlit:latest
docker push gcr.io/mjs-datavisualisation/mjs-streamlit:latest
gcloud run deploy mjs-datavisualisation  \
--image gcr.io/mjs-datavisualisation/mjs-streamlit:latest \
--platform managed  \
--allow-unauthenticated \ 
--region europe-west4 \
--memory 2Gi --timeout=900
```

# Commands for image update
```
gcloud auth login
gcloud config set project mjs-datavisualisation
docker build -t mjs-streamlit .
docker tag mjs-streamlit:latest gcr.io/mjs-datavisualisation/mjs-streamlit:latest
docker push gcr.io/mjs-datavisualisation/mjs-streamlit:latest
gcloud run deploy mjs-datavisualisation  \
--image gcr.io/mjs-datavisualisation/mjs-streamlit:latest \
--platform managed  \
--region europe-west4 \
--memory 2Gi \
--timeout=900
```