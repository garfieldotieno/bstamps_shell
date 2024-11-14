FROM openjdk:8-jdk

# Copy the s3proxy binary
ADD https://github.com/andrewgaul/s3proxy/releases/download/s3proxy-1.6.0/s3proxy /opt/s3proxy
RUN chmod +x /opt/s3proxy

# Copy the s3proxy configuration file
COPY s3proxy.conf /opt/s3proxy.conf

# Expose port 80 for S3Proxy
EXPOSE 8020

# Start S3Proxy with the provided configuration file
CMD ["/opt/s3proxy", "--properties", "/opt/s3proxy.conf"]
