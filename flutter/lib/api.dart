import 'dart:convert';
import 'package:http/http.dart' as http;

class OlymposApi {
  OlymposApi({this.baseUrl = 'http://localhost:8000'});
  final String baseUrl;

  Future<Map<String, dynamic>> _json(String path,
      {String method = 'GET', Map<String, dynamic>? body}) async {
    final uri = Uri.parse('$baseUrl$path');
    final headers = {'Content-Type': 'application/json'};
    final response = method == 'POST'
        ? await http.post(uri, headers: headers, body: jsonEncode(body ?? {}))
        : await http.get(uri, headers: headers);
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode >= 400) {
      throw Exception(data['detail'] ?? 'API error');
    }
    return data;
  }

  Future<String> register({
    required String gender,
    required String target,
    required String role,
    required String ageBand,
    required bool portraitOptIn,
  }) async {
    final data = await _json('/v1/participants', method: 'POST', body: {
      'gender_identity': gender,
      'target_genders': [target],
      'role': role,
      'age_band': ageBand,
      'area': '東京都',
      'interested_modes': [gender == 'male' ? 'ZEUS' : 'APHRODITE'],
      'required_age_bands': [ageBand],
      'preferred_age_bands': [ageBand],
      'availability': [
        '2026-10-03T10', '2026-10-04T13', '2026-10-10T10'
      ],
      'portrait_opt_in': portraitOptIn,
    });
    return data['id'] as String;
  }

  Future<Map<String, dynamic>> kpis() => _json('/v1/kpis');
  Future<Map<String, dynamic>> simulate() =>
      _json('/v1/simulations', method: 'POST');
}
