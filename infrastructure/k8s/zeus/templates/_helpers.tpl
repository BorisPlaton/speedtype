{{/*
General chart name
*/}}
{{- define "zeus.name" -}}
{{- .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Release name
*/}}
{{- define "zeus.release_name" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Specific version chart name
*/}}
{{- define "zeus.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | trunc 63 }}
{{- end }}

{{/*
Common labels used in all zeus pods
*/}}
{{- define "zeus.labels" -}}
helm.sh/chart: {{ include "zeus.chart" . }}
{{ include "zeus.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/component: {{ .Values.zeus.labels.component }}
app.kubernetes.io/part-of: {{ .Values.zeus.labels.part_of }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels for zeus pods
*/}}
{{- define "zeus.selectorLabels" -}}
app.kubernetes.io/name: {{ include "zeus.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Kubernetes service account name
*/}}
{{- define "zeus.serviceAccountName" -}}
{{- printf "%s-%s-ksa" .Chart.Name .Values.environment }}
{{- end }}
