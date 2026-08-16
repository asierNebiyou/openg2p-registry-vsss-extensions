{{/*
Common environment for all connector roles (api / worker / beat / consumer).

The connector service reads flat CONNECTOR_* env vars (no per-role prefixes).
All names are release-scoped so two registry instances in one namespace get
independent connector stacks:
  - DB:      <release>_connector on the shared PostgreSQL host (provisioned
             by this chart's postgres-init entry, secret <release>-connector)
  - Redis:   this release's own redis (db /1 to stay clear of the registry
             celery apps which use db /0)
  - Partner: this release's partner-api Service (in-cluster, no ingress hop)
*/}}
{{- define "connector.commonEnv" -}}
- name: CONNECTOR_DB_DRIVER
  value: {{ .Values.connector.commonEnv.dbDriver | quote }}
- name: CONNECTOR_DB_HOSTNAME
  value: {{ .Values.global.postgresqlHost | quote }}
- name: CONNECTOR_DB_PORT
  value: {{ .Values.global.registryDBPort | quote }}
- name: CONNECTOR_DB_USERNAME
  value: {{ tpl .Values.global.connectorDBUser $ | quote }}
- name: CONNECTOR_DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ tpl .Values.global.connectorDBSecret $ | quote }}
      key: {{ tpl .Values.global.connectorDBUserPasswordKey $ | quote }}
- name: CONNECTOR_DB_DBNAME
  value: {{ tpl .Values.global.connectorDB $ | quote }}
- name: CONNECTOR_PARTNER_INGEST_BASE_URL
  value: {{ tpl .Values.connector.partnerIngestBaseUrl $ | quote }}
- name: CONNECTOR_CELERY_BROKER_URL
  value: {{ printf "redis://%s:6379/1" (tpl .Values.global.redisInstallationName $) | quote }}
- name: CONNECTOR_CELERY_RESULT_BACKEND
  value: {{ printf "redis://%s:6379/1" (tpl .Values.global.redisInstallationName $) | quote }}
- name: CONNECTOR_LOG_LEVEL
  value: {{ .Values.connector.commonEnv.logLevel | quote }}
- name: CONNECTOR_STORE_RUN_PAYLOADS
  value: {{ .Values.connector.commonEnv.storeRunPayloads | quote }}
- name: CONNECTOR_STRICT_INCREMENTAL
  value: {{ .Values.connector.commonEnv.strictIncremental | quote }}
- name: CONNECTOR_FULL_SCAN_ON_INCREMENTAL_UNSUPPORTED
  value: {{ .Values.connector.commonEnv.fullScanOnIncrementalUnsupported | quote }}
- name: CONNECTOR_METRICS_ENABLED
  value: {{ .Values.connector.commonEnv.metricsEnabled | quote }}
- name: CONNECTOR_CORS_ORIGINS
  value: {{ printf "https://%s" (tpl .Values.global.connectorHostname $) | quote }}
{{- range $k, $v := .Values.connector.extraEnvVars }}
- name: {{ $k }}
  value: {{ tpl (toString $v) $ | quote }}
{{- end }}
{{- end -}}

{{/*
Postgres wait init-container shared by all connector roles.
*/}}
{{- define "connector.postgresCheckerInit" -}}
- name: postgres-checker
  image: {{ .Values.connector.postgresCheckerInit.image | quote }}
  imagePullPolicy: IfNotPresent
  command: ["sh"]
  args:
    - -c
    - >-
      until pg_isready -U ${CONNECTOR_DB_USERNAME} -h ${CONNECTOR_DB_HOSTNAME}
      -p ${CONNECTOR_DB_PORT:-5432} -d ${CONNECTOR_DB_DBNAME};
      do sleep 3; done
  env:
    {{- include "connector.commonEnv" . | nindent 4 }}
{{- end -}}

{{- define "connector.labels" -}}
app.kubernetes.io/name: connector
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}

{{- define "connector.selectorLabels" -}}
app.kubernetes.io/name: connector
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "connector.serviceAccountName" -}}
{{- printf "%s-connector" .Release.Name -}}
{{- end -}}

{{- define "connector.imagePullSecrets" -}}
{{- if .Values.connector.image.PullSecrets }}
imagePullSecrets:
  - name: {{ .Values.connector.image.PullSecrets }}
{{- end }}
{{- end -}}
