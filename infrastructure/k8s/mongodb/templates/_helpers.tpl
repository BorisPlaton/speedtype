{{/*
General chart name
*/}}
{{- define "mongodb.name" -}}
{{- .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Release name
*/}}
{{- define "mongodb.release_name" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Specific version chart name
*/}}
{{- define "mongodb.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | trunc 63 }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mongodb.labels" -}}
helm.sh/chart: {{ include "mongodb.chart" . }}
{{ include "mongodb.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/component: {{ .Values.mongodb.labels.component }}
app.kubernetes.io/part-of: {{ .Values.mongodb.labels.part_of }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mongodb.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mongodb.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
GCP Secret Name for MongoDB Password
*/}}
{{- define "mongodb.secrets.password" -}}
{{- printf "%s%s" .Values.secrets.gcpNames.mongodbPassword .Values.environment | trunc 63 }}
{{- end }}
