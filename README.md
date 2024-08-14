# Context Extender

A Django app designed for Open edX to extend the context in specific views, enabling the inclusion of additional data in templates. This app is particularly useful for extending the context of certificates, course emails, and other custom views without modifying the edx-platform source code.

## Features

- **Context Processors**: Extend the context for specific views like certificate rendering or course emails.
- **Customizable**: Easily add your custom context processors by modifying the settings.
- **Template Example**: Includes an example template for certificates in the `certificate_template` folder.

## Requirements

To use the certificate-related context extensions provided by context-extender, you must have the following apps installed in your LMS:

- [`eol_sso_login`](https://github.com/eol-uchile/eol_sso_login)
- [`eol_course_program`](https://github.com/eol-uchile/eol-course-program-xblock)

## Installation

1. **Install the App**:  
   Add the `context-extender` app to your Open edX platform by including it in your requirements file or by directly placing it in your project’s apps directory.

2. **Add to `INSTALLED_APPS`**:  
   Ensure that `context_extender` is included in the `INSTALLED_APPS` setting of your Open edX project:

   ```python
   INSTALLED_APPS += [
       'context_extender',
   ]
   ```

## Configuration

### Setting Up Context Extensions

To extend the context in specific views, follow these steps:

1. **Modify `settings/common.py`**:  
   If you plan to add new context extensions, define your context processors in the `settings/common.py` file.

   Example:

   ```python
   # context_extender/settings/common.py

   def plugin_settings(settings):
       # Add your context processors here
       settings.TEMPLATES[0]['OPTIONS']['context_processors'].append(
           'context_extender.context_processors.add_student_grade'
       )
       settings.TEMPLATES[0]['OPTIONS']['context_processors'].append(
           'context_extender.context_processors.add_student_program_grade'
       )
    ```
This ensures that your custom context processors are automatically loaded and applied.

2. **Extending Context in Other Apps**:  
   The `context-extender` app can be used in other apps like course emails. To do this, implement your custom context processors for the specific views you want to extend.

   Example for extending context in a course email view:

   ```python
   # courseemail/context_processors.py

   def add_course_email_context(request):
       context = {}
       # Add custom context logic here
       context['custom_data'] = "Custom value"
       return context
    ```
    Then, add this processor to the `plugin_settings` in `settings/common.py`:

    ```python
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append(
        'courseemail.context_processors.add_course_email_context'
    )
    ```

## Usage

Once installed and configured, the `context-extender` app will automatically inject the specified data into the context of the targeted views. This allows you to use the extended context directly in Mako templates, which means you can modify templates without needing to alter the backend of your Open edX platform.

### Example Use Case

* **Certificates**: Automatically adds student grades and program-related information to certificate views, which you can then use in Mako templates to customize the certificate display.

* **Course Emails**: Extend the context of course emails to include additional custom data that can be used directly in the Mako templates without modifying backend code.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the AGPL v3 License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue on the GitHub repository.
