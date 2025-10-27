import animals_web_generator

def main():
    name = input("Enter the animal name to search: ").strip()
    template_path = "animals_template.html"
    output_path = "output.html"
    print(f"Searching for '{name}' ...")
    data = animals_web_generator.get_animals(name)
    snippet = animals_web_generator.render_animals_html(data, name)
    animals_web_generator.inject_into_html(template_path, output_path, snippet)
    print(f"Done! Results written to {output_path}")

if __name__ == "__main__":
    main()
