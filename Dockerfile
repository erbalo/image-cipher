FROM public.ecr.aws/lambda/python:3.9-x86_64

# copy all code and lambda handler
COPY internal/ internal/
COPY entrypoint/ entrypoint/
COPY requirements.txt .

# install packages
# RUN yum install -y gcc-c++ pkgconfig poppler-cpp-devel
# RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install -r requirements.txt

# run lambda handler
CMD ["entrypoint.sns.handler"]
