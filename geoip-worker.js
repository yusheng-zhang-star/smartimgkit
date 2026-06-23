export default {
  fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Only redirect root pages, not API calls, files, etc.
    if (path === '/' || path === '') {
      const country = request.cf?.country?.toLowerCase() || '';

      // Spanish-speaking countries
      const spanishCountries = ['es', 'ar', 'mx', 'co', 'cl', 'pe', 've', 'ec', 'gt', 'cu', 'bo', 'do', 'hn', 'py', 'sv', 'ni', 'cr', 'pa', 'uy', 'pr', 'gq'];
      
      // Portuguese-speaking (Brazil)
      const portugueseCountries = ['br'];
      
      // Indonesian
      const indonesianCountries = ['id'];

      let redirectTo = null;

      if (spanishCountries.includes(country)) {
        redirectTo = '/es/';
      } else if (portugueseCountries.includes(country)) {
        redirectTo = '/pt/';
      } else if (indonesianCountries.includes(country)) {
        redirectTo = '/id/';
      }

      if (redirectTo) {
        return Response.redirect(new URL(redirectTo, url.origin), 302);
      }
    }

    // Forward all other requests normally
    return fetch(request);
  }
};
