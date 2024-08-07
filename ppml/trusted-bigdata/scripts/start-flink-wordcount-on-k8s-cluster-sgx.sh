export secure_password=`openssl rsautl -inkey /ppml/password/key.txt -decrypt </ppml/password/output.bin`
$FLINK_HOME/bin/flink run-application \
    --target kubernetes-application \
    -Dkubernetes.sgx.enabled=true \
    -Djobmanager.memory.process.size=4g \
    -Dtaskmanager.memory.process.size=4g \
    -Dio.tmp.dirs=/ppml/encrypted-fs \
    -Dkubernetes.flink.conf.dir=/ppml/flink/conf \
    -Dkubernetes.entry.path="/opt/flink-entrypoint.sh" \
    -Dkubernetes.jobmanager.service-account=spark \
    -Dkubernetes.taskmanager.service-account=spark \
    -Dkubernetes.cluster-id=wordcount-example-flink-cluster \
    -Dkubernetes.container.image.pull-policy=Always \
    -Dkubernetes.pod-template-file.jobmanager=/ppml/flink-k8s-template.yaml \
    -Dkubernetes.pod-template-file.taskmanager=/ppml/flink-k8s-template.yaml \
    -Dkubernetes.container.image=intelanalytics/bigdl-ppml-trusted-bigdata-gramine-reference:latest \
    -Dheartbeat.timeout=10000000 \
    -Dheartbeat.interval=10000000 \
    -Dakka.ask.timeout=10000000ms \
    -Dakka.lookup.timeout=10000000ms \
    -Dslot.request.timeout=10000000 \
    -Dtaskmanager.slot.timeout=10000000 \
    -Dkubernetes.websocket.timeout=10000000 \
    -Dtaskmanager.registration.timeout=10000000 \
    -Dresourcemanager.taskmanager-timeout=10000000 \
    -Dtaskmanager.network.request-backoff.max=10000000 \
    -Dresourcemanager.taskmanager-registration.timeout=10000000 \
    -Djobmanager.adaptive-scheduler.resource-wait-timeout=10000000 \
    -Djobmanager.adaptive-scheduler.resource-stabilization-timeout=10000000 \
    -Dsecurity.ssl.internal.enabled=true \
    -Dsecurity.ssl.internal.keystore=/ppml/flink/keys/flink_internal.keystore \
    -Dsecurity.ssl.internal.truststore=/ppml/flink/keys/flink_internal.keystore \
    -Dsecurity.ssl.internal.keystore-password=$secure_password \
    -Dsecurity.ssl.internal.truststore-password=$secure_password \
    -Dsecurity.ssl.internal.key-password=$secure_password \
    local:///ppml/flink/examples/streaming/WordCount.jar