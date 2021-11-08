from django.http import HttpResponse


class stripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    def __init__(self, request):
        # in case we need to access any attribute from the stripe request
        self.request = request

    def handle_event(self, event):
        """
        Handle generic/unknown/unexpected webhook events
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )