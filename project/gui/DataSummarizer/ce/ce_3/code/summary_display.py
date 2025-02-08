class SummaryDisplay:
    def display_summary(self, summary: dict) -> None:
        """Displays the generated summary in a text area."""
        for variable, stats in summary.items():
            print(f"Summary for {variable}:")
            if isinstance(stats, dict):
                for key, value in stats.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {stats}")
            print("\n")